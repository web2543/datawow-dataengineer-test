from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
import glob
import datetime as dt

USER='postgres'
PASSWORD='123456789'
HOST='warehouse'
DATA_PATH='/opt/airflow/data_sample'

@task(task_id='Data_dict')
def data_dict(path:list):
    import pandas as pd
    from sqlalchemy import create_engine
    engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/postgres")
    product_set=set()
    department_set=set()
    for i in range(100):
        df=pd.read_parquet(path[i])
        product_i_set=set(df['product_name'].unique())
        department_i_set=set(df['department_name'].unique())
        product_set=product_set.union(product_i_set)
        department_set=department_set.union(department_i_set)
    product_map={v:i for i,v in enumerate(product_set)}
    dfz=pd.Series(product_map).to_frame().reset_index()
    dfz.rename({"index":"product_name",0:'product_id'},axis=1,inplace=True)
    dfz[['product_id','product_name']].to_sql('products',engine,if_exists='append',index=False,method='multi')
    department_map={v:i for i,v in enumerate(department_set)}
    dfz=pd.Series(department_map).to_frame().reset_index()
    dfz.rename({"index":"department_name",0:'department_id'},axis=1,inplace=True)
    dfz[['department_id','department_name']].to_sql('departments',engine,if_exists='append',index=False,method='multi')
    return {'product':product_map,'department':department_map}

@task(task_id="ETL")
def ETL_pipeline(product_map,department_map,path):
    import pandas as pd
    from sqlalchemy import create_engine
    engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/postgres")
    for i in path:
        df=pd.read_parquet(i)
        df['department_id']=df['department_name'].apply(lambda x: department_map[x])
        df['product_id']=df['product_name'].apply(lambda x: product_map[x])
        df.rename({'create_at':"create_date",'product_expire':"expired_date"},axis=1,inplace=True)
        df[['sensor_serial',"create_date","expired_date",'department_id','product_id']].to_sql('items',engine,if_exists='append',index=False,method='multi')




default_args={
    "retries": 2,
    'retry_delay': dt.timedelta(minutes=10),
    'owner': 'datawow'
}

with DAG(
    'ETL_dag',
    start_date=dt.datetime(2023,9,12),
):
    path=glob.glob(DATA_PATH)
    map_dict=data_dict(path)
    spilt=[path[i:i + 10] for i in range(0, len(path), 10)]
    spilt_dags=[]
    for i in spilt:
        etl=ETL_pipeline(map_dict['product'],map_dict['department'],i)
        spilt_dags.append(etl)

map_dict>>spilt_dags



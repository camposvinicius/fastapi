from fastapi import APIRouter,FastAPI
import awswrangler as wr
import boto3
from dotenv import load_dotenv
import os

app = FastAPI()

router1 = APIRouter()
router2 = APIRouter()
router3 = APIRouter()

load_dotenv()

session = boto3.Session(aws_access_key_id = os.getenv('aws_access_key_id'),
                        aws_secret_access_key = os.getenv('aws_secret_access_key'), 
                        region_name = os.getenv('region_name'))

@router1.get('/Search_Databases')
async def list_databases():
    return wr.catalog.databases(boto3_session=session).to_dict(orient='records')

@router2.get('/Search_Names_Athena')
async def idpassenger(passengerid: int):
    QueryString = f"SELECT name FROM default.titanicdelta WHERE passengerid = {passengerid}"
    return wr.athena.read_sql_query(sql=QueryString, database='default', boto3_session=session)\
                    .to_dict(orient="records")

@router3.get('/Search_Items_Dynamodb')
async def names(nome:str):
    client = boto3.client('dynamodb',aws_access_key_id = os.getenv('aws_access_key_id'),
                        aws_secret_access_key = os.getenv('aws_secret_access_key'), 
                        region_name = os.getenv('region_name'))
    res = dict(client.get_item(TableName = 'vini-teste', Key={'name':{'S':str(f'{nome}')}}))
    username = res['Item']['username']['S']
    email = res['Item']['email']['S']
    return f'username: {username}', f'email: {email}'

app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
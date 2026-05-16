(venv) PS C:\Users\Rachid\Documents\HACKAHERO\backend> pip install -r requirements.txt
Collecting fastapi==0.111.0 (from -r requirements.txt (line 1))
  Using cached fastapi-0.111.0-py3-none-any.whl.metadata (25 kB)
Collecting uvicorn==0.29.0 (from uvicorn[standard]==0.29.0->-r requirements.txt (line 2))
  Using cached uvicorn-0.29.0-py3-none-any.whl.metadata (6.3 kB)
Collecting sqlalchemy==2.0.30 (from -r requirements.txt (line 3))
  Using cached SQLAlchemy-2.0.30-cp312-cp312-win_amd64.whl.metadata (9.8 kB)
Collecting alembic==1.13.1 (from -r requirements.txt (line 4))
  Using cached alembic-1.13.1-py3-none-any.whl.metadata (7.4 kB)
Collecting psycopg2-binary==2.9.9 (from -r requirements.txt (line 5))
  Using cached psycopg2_binary-2.9.9-cp312-cp312-win_amd64.whl.metadata (4.6 kB)
Collecting python-jose==3.3.0 (from python-jose[cryptography]==3.3.0->-r requirements.txt (line 6))
  Using cached python_jose-3.3.0-py2.py3-none-any.whl.metadata (5.4 kB)
Collecting passlib==1.7.4 (from passlib[bcrypt]==1.7.4->-r requirements.txt (line 7))
  Using cached passlib-1.7.4-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting pydantic==2.7.1 (from pydantic[email]==2.7.1->-r requirements.txt (line 8))
  Using cached pydantic-2.7.1-py3-none-any.whl.metadata (107 kB)
Collecting pydantic-settings==2.2.1 (from -r requirements.txt (line 9))
  Using cached pydantic_settings-2.2.1-py3-none-any.whl.metadata (3.1 kB)
Collecting python-multipart==0.0.9 (from -r requirements.txt (line 10))
  Using cached python_multipart-0.0.9-py3-none-any.whl.metadata (2.5 kB)
Collecting mistralai==1.7.0 (from -r requirements.txt (line 11))
  Using cached mistralai-1.7.0-py3-none-any.whl.metadata (30 kB)
Collecting pillow==10.3.0 (from -r requirements.txt (line 12))
  Using cached pillow-10.3.0-cp312-cp312-win_amd64.whl.metadata (9.4 kB)
Collecting httpx==0.28.1 (from -r requirements.txt (line 13))
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting starlette<0.38.0,>=0.37.2 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached starlette-0.37.2-py3-none-any.whl.metadata (5.9 kB)
Collecting typing-extensions>=4.8.0 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting fastapi-cli>=0.0.2 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached fastapi_cli-0.0.24-py3-none-any.whl.metadata (6.4 kB)
Collecting jinja2>=2.11.2 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting ujson!=4.0.2,!=4.1.0,!=4.2.0,!=4.3.0,!=5.0.0,!=5.1.0,>=4.0.1 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached ujson-5.12.1-cp312-cp312-win_amd64.whl.metadata (9.8 kB)
Collecting orjson>=3.2.1 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached orjson-3.11.9-cp312-cp312-win_amd64.whl.metadata (43 kB)
Collecting email_validator>=2.0.0 (from fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached email_validator-2.3.0-py3-none-any.whl.metadata (26 kB)
Collecting annotated-types>=0.4.0 (from pydantic==2.7.1->pydantic[email]==2.7.1->-r requirements.txt (line 8))
  Using cached annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.18.2 (from pydantic==2.7.1->pydantic[email]==2.7.1->-r requirements.txt (line 8))
  Using cached pydantic_core-2.18.2-cp312-none-win_amd64.whl.metadata (6.7 kB)
Collecting click>=7.0 (from uvicorn==0.29.0->uvicorn[standard]==0.29.0->-r requirements.txt (line 2))
  Using cached click-8.3.3-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn==0.29.0->uvicorn[standard]==0.29.0->-r requirements.txt (line 2))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting greenlet!=0.4.17 (from sqlalchemy==2.0.30->-r requirements.txt (line 3))
  Using cached greenlet-3.5.0-cp312-cp312-win_amd64.whl.metadata (3.8 kB)
Collecting Mako (from alembic==1.13.1->-r requirements.txt (line 4))
  Using cached mako-1.3.12-py3-none-any.whl.metadata (2.9 kB)
Collecting ecdsa!=0.15 (from python-jose==3.3.0->python-jose[cryptography]==3.3.0->-r requirements.txt (line 6))
  Using cached ecdsa-0.19.2-py2.py3-none-any.whl.metadata (29 kB)
Collecting rsa (from python-jose==3.3.0->python-jose[cryptography]==3.3.0->-r requirements.txt (line 6))
  Using cached rsa-4.9.1-py3-none-any.whl.metadata (5.6 kB)
Collecting pyasn1 (from python-jose==3.3.0->python-jose[cryptography]==3.3.0->-r requirements.txt (line 6))
  Using cached pyasn1-0.6.3-py3-none-any.whl.metadata (8.4 kB)
Collecting python-dotenv>=0.21.0 (from pydantic-settings==2.2.1->-r requirements.txt (line 9))
  Using cached python_dotenv-1.2.2-py3-none-any.whl.metadata (27 kB)
Collecting eval-type-backport>=0.2.0 (from mistralai==1.7.0->-r requirements.txt (line 11))
  Using cached eval_type_backport-0.3.1-py3-none-any.whl.metadata (2.4 kB)
INFO: pip is looking at multiple versions of mistralai to determine which version is compatible with other requirements. This could take a while.
ERROR: Cannot install -r requirements.txt (line 1), -r requirements.txt (line 11), -r requirements.txt (line 9) and pydantic==2.7.1 because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested pydantic==2.7.1
    fastapi 0.111.0 depends on pydantic!=1.8, !=1.8.1, !=2.0.0, !=2.0.1, !=2.1.0, <3.0.0 and >=1.7.4
    pydantic-settings 2.2.1 depends on pydantic>=2.3.0
    mistralai 1.7.0 depends on pydantic>=2.10.3

Additionally, some packages in these conflicts have no matching distributions available for your environment:
    pydantic

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip to attempt to solve the dependency conflict

ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts
(venv) PS C:\Users\Rachid\Documents\HACKAHERO\backend> 
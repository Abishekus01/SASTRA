from typing import Any, Dict, List, NoReturn, Optional, TypeAlias, Union, Tuple
import pymysql
import werkzeug

Connection: TypeAlias = pymysql.connections.Connection
Cursor: TypeAlias = pymysql.cursors.DictCursor

Response: TypeAlias = werkzeug.wrappers.Response
NotFound: TypeAlias = werkzeug.exceptions.NotFound

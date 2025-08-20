import argparse
import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import Schema, fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


app = Flask(__name__)

# Initialize Marshmallow
ma = Marshmallow(app)

# Define Schema classes
class UserInfoSchema(Schema):
    name = fields.Str(required=True)

class UserResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)

class UserCreateSchema(Schema):
    username = fields.Str(required=True, )
    email = fields.Email(required=True)
    
   

class UserUpdateSchema(Schema):
    username = fields.Str(validate=lambda x: len(x) >= 3 if x else None)
    email = fields.Email()
    
   

class MethodResponseSchema(Schema):
    method = fields.Str(required=True)

class FrameworkResponseSchema(Schema):
    framework = fields.Str(required=True)

class MessageResponseSchema(Schema):
    message = fields.Str(required=True)

class UserIdSchema(Schema):
    id = fields.Str(required=True)

class UserIdParamSchema(Schema):
    user_id = fields.Int(required=True, validate=lambda x: x > 0)
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()

# 解析命令行参数
parser = argparse.ArgumentParser(description="Flask Demo Server")
parser.add_argument(
    "--document",
    type=str,
    default="false",
    help="Enable swagger documentation (true/false)",
)
parser.add_argument(
    "--debug", type=str, default="false", help="Enable debug mode (true/false)"
)
parser.add_argument("--port", type=int, default=1999, help="Port to listen on")
args = parser.parse_args()

# 根据命令行参数决定是否启用Swagger
if args.document.lower() == "true":
    # Swagger配置
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Flask Demo API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# 根据命令行参数决定是否创建swagger.json路由
if args.document.lower() == "true":
    @app.route("/static/swagger.json")
    def swagger_json():
        json_text = """
      

{
  "openapi": "3.1.0",
  "info": {
    "title": "flask-demo-project",
    "description": "",
    "version": "1.0.0"
  },
  "tags": [],
  "paths": {
    "/hello": {
      "post": {
        "summary": "返回Hello World消息（POST方法）",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "message"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "message"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338648240-run"
      }
    },
    "/": {
      "get": {
        "summary": "返回Hello World消息",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "message"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "message"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338648322-run"
      }
    },
    "/hi": {
      "get": {
        "summary": "返回Hi消息",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "message"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "message"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338648421-run"
      }
    },
    "/user/{id}": {
      "get": {
        "summary": "根据用户ID返回对应的框架名称",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "用户ID",
            "required": true,
            "example": "",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "framework": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "framework"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "framework"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338659904-run"
      }
    },
    "/api/users": {
      "get": {
        "summary": "获取所有用户列表",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "email": {
                        "type": "string"
                      },
                      "id": {
                        "type": "integer"
                      },
                      "username": {
                        "type": "string"
                      }
                    },
                    "x-apifox-ignore-properties": [],
                    "x-apifox-orders": [
                      "email",
                      "id",
                      "username"
                    ]
                  }
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338737339-run"
      },
      "post": {
        "summary": "创建新用户",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "email": {
                    "type": "string"
                  },
                  "username": {
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "email"
                ],
                "type": "object",
                "x-apifox-orders": [
                  "email",
                  "username"
                ],
                "x-apifox-ignore-properties": []
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "用户创建成功",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "email": {
                      "type": "string"
                    },
                    "id": {
                      "type": "integer"
                    },
                    "username": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "email",
                    "id",
                    "username"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "email",
                    "id",
                    "username"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          },
          "400": {
            "description": "请求参数错误",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {},
                  "x-apifox-orders": [],
                  "x-apifox-ignore-properties": []
                }
              }
            },
            "headers": {},
            "x-apifox-name": "请求有误"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338737340-run"
      }
    },
    "/api/users/{user_id}": {
      "delete": {
        "summary": "删除用户",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [
          {
            "name": "user_id",
            "in": "path",
            "description": "用户ID",
            "required": true,
            "example": 0,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "删除成功",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "message": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "id",
                    "message"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "id",
                    "message"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          },
          "404": {
            "description": "用户不存在",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {},
                  "x-apifox-orders": [],
                  "x-apifox-ignore-properties": []
                }
              }
            },
            "headers": {},
            "x-apifox-name": "记录不存在"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338737341-run"
      },
      "get": {
        "summary": "根据ID获取用户信息",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [
          {
            "name": "user_id",
            "in": "path",
            "description": "用户ID",
            "required": true,
            "example": 0,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "email": {
                      "type": "string"
                    },
                    "id": {
                      "type": "integer"
                    },
                    "username": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "email",
                    "id",
                    "username"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "email",
                    "id",
                    "username"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          },
          "404": {
            "description": "用户不存在",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {},
                  "x-apifox-orders": [],
                  "x-apifox-ignore-properties": []
                }
              }
            },
            "headers": {},
            "x-apifox-name": "记录不存在"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338737342-run"
      },
      "put": {
        "summary": "更新用户信息",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [
          {
            "name": "user_id",
            "in": "path",
            "description": "用户ID",
            "required": true,
            "example": 0,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "properties": {
                  "email": {
                    "type": "string"
                  },
                  "username": {
                    "type": "string"
                  }
                },
                "type": "object",
                "x-apifox-orders": [
                  "email",
                  "username"
                ],
                "x-apifox-ignore-properties": []
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "更新成功",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "email": {
                      "type": "string"
                    },
                    "id": {
                      "type": "integer"
                    },
                    "username": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "email",
                    "id",
                    "username"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "email",
                    "id",
                    "username"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          },
          "400": {
            "description": "请求参数错误",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {},
                  "x-apifox-orders": [],
                  "x-apifox-ignore-properties": []
                }
              }
            },
            "headers": {},
            "x-apifox-name": "请求有误"
          },
          "404": {
            "description": "用户不存在",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {},
                  "x-apifox-orders": [],
                  "x-apifox-ignore-properties": []
                }
              }
            },
            "headers": {},
            "x-apifox-name": "记录不存在"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338737343-run"
      }
    },
    "/method": {
      "get": {
        "summary": "返回请求方法（GET）",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "method": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "method"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "method"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338678891-run"
      },
      "post": {
        "summary": "返回请求方法（POST）",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "method": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "method"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "method"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338678892-run"
      }
    },
    "/user-info": {
      "get": {
        "summary": "返回用户信息",
        "deprecated": false,
        "description": "",
        "tags": [],
        "parameters": [],
        "responses": {
          "200": {
            "description": "成功响应",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "x-apifox-ignore-properties": [],
                  "x-apifox-orders": [
                    "name"
                  ]
                }
              }
            },
            "headers": {},
            "x-apifox-name": "成功"
          }
        },
        "security": [],
        "x-apifox-folder": "",
        "x-apifox-status": "released",
        "x-run-in-apifox": "https://app.apifox.com/web/project/6978653/apis/api-338737344-run"
      }
    }
  },
  "webhooks": {},
  "components": {
    "schemas": {},
    "securitySchemes": {}
  },
  "servers": [],
  "security": []
}



        """
        swagger_spec = json.loads(json_text)
        return jsonify(swagger_spec)


# 保持原有的路由
@app.route("/")
def index():
    schema = MessageResponseSchema()
    result = schema.dump({"message": "Hello, World!"})
    return jsonify(result)


@app.route("/hi")
def hi():
    schema = MessageResponseSchema()
    result = schema.dump({"message": "Hi!"})
    return jsonify(result)


@app.route("/hello", methods=["POST"])
def hello():
    schema = MessageResponseSchema()
    result = schema.dump({"message": "Hello, World!"})
    return jsonify(result)


@app.route("/user/<id>")
def user(id):
    # Validate path parameter
    try:
        param_schema = UserIdSchema()
        param_schema.load({"id": id})
    except ValidationError as err:
        return jsonify({"error": "invalid id parameter", "details": err.messages}), 400
    
    # Determine framework based on id
    if id == "1":
        framework = "python"
    elif id == "2":
        framework = "django"
    elif id == "3":
        framework = "flask"
    else:
        framework = "hello world"
    
    schema = FrameworkResponseSchema()
    result = schema.dump({"framework": framework})
    return jsonify(result)


@app.route("/method", methods=["GET", "POST"])
def get_method():
    schema = MethodResponseSchema()
    result = schema.dump({"method": request.method})
    return jsonify(result)


@app.route("/user-info", methods=["get"])
def user_info():
    schema = UserInfoSchema()
    result = schema.dump({"name": "张三"})
    return jsonify(result)


# User RESTful API endpoints
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    schema = UserResponseSchema(many=True)
    result = schema.dump(users)
    return jsonify(result)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    
    # Validate request data
    try:
        schema = UserCreateSchema()
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=validated_data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=validated_data["username"], email=validated_data["email"])
    db.session.add(user)
    db.session.commit()

    # Return response with schema
    response_schema = UserResponseSchema()
    result = response_schema.dump(user)
    return jsonify(result), 201


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    schema = UserResponseSchema()
    result = schema.dump(user)
    return jsonify(result)


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate request data
    try:
        schema = UserUpdateSchema()
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400

    if "username" in validated_data:
        # 检查新用户名是否与其他用户冲突
        existing_user = User.query.filter_by(username=validated_data["username"]).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "Username already exists"}), 400
        user.username = validated_data["username"]

    if "email" in validated_data:
        user.email = validated_data["email"]

    db.session.commit()
    
    # Return response with schema
    response_schema = UserResponseSchema()
    result = response_schema.dump(user)
    return jsonify(result)

class DeleteResponseSchema(Schema):
    message = fields.Str(required=True)
    id = fields.Int(required=True)
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    # Return response with schema
    schema = DeleteResponseSchema()
    result = schema.dump({"message": "User deleted successfully", "id": user_id})
    return jsonify(result), 200


def main():
    debug_mode = args.debug.lower() == "true"
    print(args)
    app.run(debug=debug_mode, port=args.port, host="0.0.0.0")


if __name__ == "__main__":
    main()

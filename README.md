# Flask Demo Project

一个简单的Flask演示项目，包含自动文件监控和应用重启功能。

## 功能特点

- 使用Flask框架构建Web应用
- 集成SQLAlchemy进行数据库操作
- 文件监控功能，修改Python文件后自动重启应用
- Swagger UI接口文档支持

## 环境要求

- Python 3.10+
- pip (Python包管理器)
- 虚拟环境工具 (可选但推荐)

## 安装步骤

1. 克隆项目到本地

```bash
git clone <repository-url>
cd flask-demo-project
```

2. 创建并激活虚拟环境

```bash
# Windows系统
python -m venv .venv
.venv\Scripts\activate.bat

# macOS/Linux系统
python3 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖包

```bash
pip install -r requirements.txt
```

## 使用方法

1. 通过文件监控器启动应用

```bash
python file_watcher.py
```

2. 应用将自动监控当前目录下的Python文件变化
3. 当检测到文件修改时，应用会自动重启
4. 在浏览器中访问: http://localhost:5000

## 项目结构

- `main.py`: 应用入口文件
- `file_watcher.py`: 文件监控器，用于自动重启应用
- `requirements.txt`: 项目依赖列表
- `instance/`: 实例配置和数据库文件

## 技术栈

- Flask 3.1.2 - Web应用框架
- Flask-SQLAlchemy 3.1.1 - ORM数据库工具
- Flask-Swagger-UI 5.21.0 - API文档生成
- Watchdog 6.0.0 - 文件系统监控

## 许可证

[MIT](LICENSE)

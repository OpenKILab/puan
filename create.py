import importlib

def create_instance_from_string(class_name):
    # 假设所有类都在 'model' 包下的以 'http_' 开头的模块中
    module_name = 'model.http_' + class_name.lower() + '_model'
    
    try:
        # 动态导入模块
        module = importlib.import_module(module_name)
        # 获取类
        cls = getattr(module, class_name)
        # 创建类的实例
        instance = cls(api_key = "")
        return instance
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error: {e}")
        return None

# 使用例
class_name = "PuanAPI"
instance = create_instance_from_string(class_name)
print(instance)

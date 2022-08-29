from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from students.models import Student
from .serializers import StudentSerializer

# Create your views here.
class Student1View(View):
    """使用序列化器进行数据的序列化操作"""
    """序列化器转换一条数据[模型转换成字典]"""
    def get(self, request, pk):
        # 接收客户端传过来的参数，进行过滤查询，先查出学生对象
        student = Student.objects.get(pk=pk)
        # 转换数据类型
        # 1.实例化序列化器类
        """
            StudentSerializer(instance=模型对象或者模型列表，客户端提交的数据，额外要传递到序列化器中使用的数据)
        """
        serializer = StudentSerializer(instance=student)

        # 2.查看序列化器的转换结果
        print(serializer.data)
        return JsonResponse(serializer.data)

class Student2View(View):
    """序列化器转换多条数据[模型转换成字典]"""
    def get(self, request):
        student_list = Student.objects.all()
        # 序列化器转换多个数据
        # many=True 表示本次序列化器转换如果有多个模型对象列参数，则必须声明 Many=True
        serializer = StudentSerializer(instance=student_list, many=True)

        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

class Student3View(View):

    def post(self, request):
        data = request.body.decode()
        # 反序列化用户提交的数据
        data_dict = json.loads(data)
        print(data_dict)

        # 调用序列化器进行实例化

        serializer = Student3Serializer(data=data_dict)

        # is_valid在执行的时候，会自动先后调用 字段的内置选项,自定义验证方法，自定义验证函数
        # 调用序列化器中写好的验证代码
        # raise_exception=True 抛出验证错误信息，并阻止代码继续往后运行
        # 验证结果
        print(serializer.is_valid(raise_exception=True))

        # 获取验证后的错误信息
        print(serializer.errors)

        # 获取验证后的客户端提交的数据
        print(serializer.validated_data)
        # save 表示让序列化器开始执行反序列化代码。create和update的代码
        serializer.save()
        # return HttpResponse(serializer.validated_data)
        return JsonResponse(serializer.validated_data)

class Student4View(View):
    def put(self, request, pk):
        data = request.body.decode()
        import json
        data_dict = json.loads(data)

        student_obj = Student.objects.get(pk=pk)
        # 有instance参数，调用save方法，就会调用update方法。
        serializer = Student3Serializer(instance=student_obj, data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()  # 触发序列器中的update方法

        return JsonResponse(serializer.validated_data)

class Student5View(View):
    def get(self, request):
        # 获取所有数据
        student_list = Student.objects.all()
        serializer = Student5Serializer(instance=student_list, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.body.decode()
        data_dict = json.loads(data)

        serializer = Student5Serializer(data=data_dict)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        return JsonResponse(serializer.data)

class Student6View(View):
    def get(self, request):
        # 获取所有数据
        student_list = Student.objects.all()

        serializer = StudentModelSerializer(instance=student_list, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.body.decode()
        data_dict = json.loads(data)

        serializer = StudentModelSerializer(data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return JsonResponse(serializer.data)


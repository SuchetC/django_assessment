from rest_framework import serializers
from .models import CollegeStream, Streams, College,  Student

class StreamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streams
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('reg_no', 'first_name', 'last_name')


class CollegeStreamSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True, source='branch.student_set')
    branch = StreamsSerializer()
    class Meta:
        model = CollegeStream
        fields = ('branch', 'students')
        
class CollegeDetailSerializer(serializers.ModelSerializer):
    college_stream = CollegeStreamSerializer(many=True, read_only=True, source='collegestream_set')

    class Meta:
        model = College
        fields = ('college_code', 'name', 'college_stream')
                            

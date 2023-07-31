from venv import logger
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .models import College, CollegeStream, Streams, Student
from .serializers import CollegeDetailSerializer, CollegeSerializer ,StreamsSerializer
import pandas as pd
import logging

# Create your views here.

class CollegeDataViewset(viewsets.ViewSet):
    
    """ A simple ViewSet for Populating data to the database """
    
    @action(detail=False, methods=['post'])
    def create_college(self, request, *args, **kwargs):
        """ Extra action for populating college data"""
        logging.info("Received a request to populate college data.")
        file = request.FILES.get('assessment')
        if not file:
            logging.error("No file was uploaded.")
            return Response({'error': 'Please upload an Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, engine='openpyxl',sheet_name="Colleges",usecols=[0,1])
            df.columns = ['cid','name']
            # print("LENGTH__________",len(df))
            
            for data in df.itertuples():
                college,created = College.objects.get_or_create(college_code=data.cid, name=data.name)
            
                if created:
                    logging.info(f"College with code {data.cid} and name '{data.name}' created.")
                else:
                    logging.info(f"College with code {data.cid} and name '{data.name}' already exists.")

        except Exception as e:
            logging.exception(f"Error processing the Excel file: {str(e)}")
            return Response({'error': 'Error processing the Excel file!'}, status=status.HTTP_400_BAD_REQUEST)

        logging.info("College Data added successfully.")
        return Response({'message': 'College Data added successfully.'}, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=['post'])
    def create_Streams(self, request, *args, **kwargs):
        """ Extra action for populating Streams data"""
        logging.info("Received a request to populate Stream data.")
        file = request.FILES.get('assessment')
        if not file:
            logging.error("No file was uploaded.")
            return Response({'error': 'Please upload an Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, engine='openpyxl',sheet_name="Streams",usecols=[0,1])
            df.columns = ['sid','name']
            # print("LENGTH__________",len(df))
            
            for data in df.itertuples():
                Stream, created = Streams.objects.get_or_create(branch_code=data.sid, name=data.name)
                if created:
                    logging.info(f"College with code {data.sid} and name '{data.name}' created.")
                else:
                    logging.info(f"College with code {data.sid} and name '{data.name}' already exists.")

        except Exception as e:
            logging.exception(f"Error processing the Excel file: {str(e)}")
            return Response({'error': 'Error processing the Excel file!'}, status=status.HTTP_400_BAD_REQUEST)
        logging.info("Strams Data added successfully.")
        return Response({'message': 'Stream Data added successfully.'}, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=['post'])
    def create_college_streaams(self, request, *args, **kwargs):
        """ Extra action for populating college_strams data"""
        logging.info("Received a request to populate Stream data.")
        file = request.FILES.get('assessment')
        if not file:
            logger.error("No file was uploaded.")
            return Response({'error': 'Please upload an Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, engine='openpyxl',sheet_name="college streaams",usecols=[0,1])
            df.columns = ['college','branch']
            # print("LENGTH__________",len(df))
            
            for data in df.itertuples():
                try:
                    college_id = College.objects.filter(name=data.college).values_list('id', flat=True).first()
                    stream_id = Streams.objects.filter(name=data.branch).values_list('id', flat=True).first()
                except :
                    IndexError
                clg_stream,created = CollegeStream.objects.get_or_create(college_id=college_id, branch_id=stream_id)               
                if created:
                    logger.info(f"College_stream with code {data.college} and name '{data.branch}' created.")
                else:
                    logger.info(f"College_stram with code {data.college} and name '{data.branch}' already exists.")
                
        except Exception as e:
            print(e)
            return Response({'error': 'Error processing the Excel file!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'College_streams Data added successfully.'}, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'])
    def create_Students(self, request, *args, **kwargs):
        """ Extra action for populating Students data"""
        logger.info("Received a request to populate students data.")
        file = request.FILES.get('assessment')
        if not file:
            logger.error("No file was uploaded.")
            return Response({'error': 'Please upload an Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file, engine='openpyxl',sheet_name="Students",usecols=[0,1,2,3,4])
            df.columns = ['rno','fname','lname','branch','colg']
            # print("LENGTH__________",len(df))
            
            for data in df.itertuples():
                try:
                   branch_id = Streams.objects.filter(name=data.branch).values_list('id', flat=True).first()
                   clg_id = College.objects.filter(name=data.colg).values_list('id',flat=True).first()
                except:
                    continue
                stud,created = Student.objects.get_or_create(reg_no = data.rno, first_name=data.fname, last_name=data.lname, branch_id=branch_id, college_id=clg_id)   
                if created:
                    logger.info(f"College with code {data.rno} and name '{data.fname}' created.")
                else:
                    logger.info(f"College with code {data.rno} and name '{data.fname}' already exists.")

            
        except Exception as e:
            logger.exception(f"Error processing the Excel file: {str(e)}")
            return Response({'error': 'Error processing the Excel file!'}, status=status.HTTP_400_BAD_REQUEST)
        logger.info("College Data added successfully.")
        return Response({'message': 'Student Data added successfully.'}, status=status.HTTP_201_CREATED)
    
    

class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    
    """  Simple viewSet to retrive College data """
    # queryset = College.objects.prefetch_related('collegestream_set__branch')
    # serializer_class = CollegeDetailSerializer
    
    serializer_class = CollegeDetailSerializer
    def get_queryset(self):
        queryset = College.objects.all()

        # Use prefetch_related to fetch related CollegeStream (branch) and Student data
        queryset = queryset.prefetch_related('collegestream_set__branch', 'student_set')


        return queryset    
        
        
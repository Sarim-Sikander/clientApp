from traceback import print_tb
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
import math
from django.utils import translation
from .models import Feedback,Feedback_percent
import PyPDF2
import docx2txt
import pickle
import os
import requests
import json
import re


def get_terms(request):
    return render(request,'TermConditions.html')

def privacypolicy(request):
  return render(request,'PrivacyPolicy.html')


def get_feeds():
    feeds=Feedback.objects.all()
    good=""
    bad=""
    
    if(feeds.count()>0):
      good=Feedback.objects.filter(feedback="Good")
      bad=Feedback.objects.filter(feedback="Bad")

      good=(good.count()*100)/feeds.count()
      bad=(bad.count()*100)/feeds.count()
    
    f_percent=Feedback_percent.objects.last()
    if(f_percent):
      try:
        f_percent.bad_percent = bad
        f_percent.good_percent = good
        f_percent.save()
      except:
        f_percent.bad_percent = 0.00
        f_percent.good_percent = 0.00
        f_percent.save()
    else:
      f_percent=Feedback_percent.objects.create(good_percent=good, bad_percent=bad);
      f_percent.save()

    return {"good":good, "bad":bad}
def home(request):
    obj=get_feeds()
    return render(request,'index.html',context={"bad_votes":obj['bad'],"good_votes":obj['good']}) 

def file_check(request):
    obj=get_feeds()
    
    if request.method == 'POST':
        try:
            request.FILES['file_id']
            result = read_pdf(request.FILES['file_id'])
            if (result == False):
                return render(request,'index.html' , context={"error":"File Formate is Not Supported !","bad_votes":obj['bad'],"good_votes":obj['good']})        
            else:
                
                # result = re.sub(r'(\r\n)+', '\n', result)
                result = re.sub(r'(\n\n)+', ' ', result)
                
                return render(request,'index.html' , context={"textarea":result,"bad_votes":obj['bad'],"good_votes":obj['good']})
        except:
            text=request.POST['text_hay']
            lenth=len(text.split(' '))
            if(lenth<200):
              return render(request,'index.html' , context={"textarea":text,'error':"Length Must be more than 200 Words","bad_votes":obj['bad'],"good_votes":obj['good']})
            max_l=int(request.POST['max_length'])
            max_l=((max_l/100) * lenth)
            result=text
            # result = re.sub(r'(\r\n)+', '\n\n', text)
            # result = re.sub(r'(\n)+', '', result)
            
            
            
            # # res=predict(text_bullet,max_length=int(math.floor(max_l)))
            # import requests
            res2 = requests.post(
                "https://api.deepai.org/api/summarization",
                data={
                    'text': result,
                },
                headers={'api-key': 'cacc1871-7ad6-4a27-b1bb-f24e7a18ed23'}
            )
            # res=[]
            # for i in result:
            #   res.append(query({"input":i}))
               
            res2=res2.json()['output']
            
            res = query({
            "inputs": [result],
              "parameters": {"do_sample": False},
              "max_length": max_l
                  })
            bullets=bullet(res[0]['summary_text'])
            # bullets=bullet(result)
            
            bestLine = query({
            "inputs": [bestLineSelection(result.split('\n'))],
              "parameters": {"do_sample": False},
              "max_length": max_l
                  })
            return render(request,'index.html' , context={"textarea":text,'res':res[0]['summary_text'],'bullet':bullets,'bestline':bestLine[0]['summary_text'],"bad_votes":obj['bad'],"good_votes":obj['good']})
    return render(request,'index.html')


# For best line
def bestLineSelection(prediction):
  maxLine = []
  for line in range(len(prediction)):
    maxLine.append(len(prediction[line]))
  max_ = max(maxLine)
  for line in range(len(prediction)):
    if max_ == len(prediction[line]):
      bestLine = prediction[line]
  return bestLine

def bullet(text):
  return list(filter(lambda x : x != '', text.split('.')))




API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
headers = {"Authorization": "Bearer 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"}

def query(payload):
  data = json.dumps(payload)
  response = requests.request("POST", API_URL, headers=headers, data=data)
  return json.loads(response.content.decode("utf-8"))





def feedback(request,pk):
  
  client_ip = request.META['REMOTE_ADDR']
  


  if request.method == 'POST':
    
    if pk=='b':
      f=Feedback.objects.filter(IP=client_ip,feedback="Bad")
      if (f):
        pass
      else:
        f=Feedback.objects.create(IP=client_ip,feedback='Bad',msg=request.POST['message'],email=request.POST['email'])
        f.save()

    

  
  if(pk=='g'):
    f=Feedback.objects.filter(IP=client_ip,feedback="Good")
    if (f):
      pass
    else:
      f=Feedback.objects.create(IP=client_ip,feedback='Good')
      f.save()
  
  obj=get_feeds()
  return render(request,'index.html' , context={"feedback":"Done","bad_votes":obj['bad'],"good_votes":obj['good']})
def read_pdf(filename):
  pdf_pages = []
  doc_pages = ''
#   pdfFileObj = open(filename, 'rb')
  
  if filename.name.split('.')[1] == 'pdf':
    # pdfFileObj = open(filename, 'wb+')
    pdfReader = PyPDF2.PdfFileReader(filename)
    
    for i in range(pdfReader.numPages):
      pageObj = pdfReader.getPage(i)
      
      result = re.sub(r'(\n)+', '\n', pageObj.extractText())
      pdf_pages.append(result)
      
    # pdfFileObj.close()
    return " ".join(pdf_pages)
  elif filename.name.split('.')[1] == 'docx':
    my_text = docx2txt.process(filename)
    doc_pages = my_text
    return doc_pages
  else:
    return False

# def predict(text, max_length=1024, n_accurate=6):
#   input = tokenizer(text, max_length=max_length,padding=True,truncation=True,return_tensors="pt")
#   ids = model.generate(input['input_ids'],num_beams=n_accurate, max_length=max_length, early_stopping=True)
#   predictions=[tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False).strip() for g in ids]
#   return predictions

  
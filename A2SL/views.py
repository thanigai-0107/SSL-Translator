from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from datetime import datetime



def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o

def home_view(request):
	return render(request,'home.html')


def animation_view(request):
	if request.method == 'POST':
		# current_date=datetime.datetime.now()
		# current_date_string=str(current_date)
		current_date_string=datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
		extension = ".txt"
		file_name = current_date_string+extension
		notes=open(file_name, 'a')
		notes.write("Notes For Reference \n")
		final_text=[]
		text = request.POST.get('sen')
		sentences=text.split(".")
		for sentence in sentences:
		#Tokenising of sentence into words
			words=word_tokenize(sentence) 
			#print(words)
			# Parts of Speech to the words
			tagged = nltk.pos_tag(words) 
			#print(tagged)
			#Removal of stop words and lemmatizing
			stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])
			interogative_words=set(["what","who","how","which","where","when","why","whose","why"])
			lr=WordNetLemmatizer()
			filtered_text=[]
			for w,p in zip(words,tagged):
				if w not in stop_words:
					if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
						filtered_text.append(lr.lemmatize(w,pos='v'))
					elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
						filtered_text.append(lr.lemmatize(w,pos='a'))
					else:
						filtered_text.append(lr.lemmatize(w))
			#print(filtered_text)
			#Dictionary to find the probable tense
			tense = {}
			tense["future"] = len([word for word in tagged if word[1] == "MD"])
			tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
			tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
			tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])
			words=filtered_text
			l=len(words)
			#Replacing "i" with "me"
			for i in range(l):
				if words[i]=="i":
					words[i]="me"
			#Placing wh words at the end of the sentence
			for i in range(l):
				if words[i] in interogative_words:
					wh_word=words[i]
					words.remove(wh_word)
					words.append(wh_word)
					#print(words)
			#Finding the tense and placing words such as "Before" for past, "Will" for future and "Now" for present continuous 
			probable_tense = max(tense,key=tense.get)
			if probable_tense == "past" and tense["past"]>=1:
				temp = ["before"]
				temp = temp + words
				words = temp
			elif probable_tense == "future" and tense["future"]>=1:
					if "will" not in words:
						temp = ["will"]
						temp = temp + words
						words = temp
					else:
						pass
			elif probable_tense == "present":
				if tense["present_continuous"]>=1:
					temp = ["now"]
					temp = temp + words
					words = temp
			final_text.append(words)
		words=list(traverse(final_text))
		filtered_text = []
		
		for w in words:
			notes.write("--"+w+"\n") 

			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		notes.close() 
		

		return render(request,'animation.html',{'words':words,'text':text})
	else:
		return render(request,'animation.html')





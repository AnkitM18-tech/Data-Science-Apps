#Import Libraries
import pandas as pd
import streamlit as stl
import altair as alt
from PIL import Image

#Page Title
image = Image.open('dna-logo.jpg')

stl.image(image,use_column_width=True)

stl.write("""
    # DNA Nucleotide Count Web App

    This App counts the nucleotide composition of query DNA!

    ***
""")

#Input Text Box
stl.header('Enter DNA Sequence')

sequence_input = ">DNA Query \nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"
sequence = stl.text_area("Sequence Input",sequence_input,height=200)
sequence = sequence.splitlines()
sequence = sequence[1:]  #skips the sequence name(first line)
sequence = ''.join(sequence) #concatenates list to string

stl.write("""
    ***
""")

#Print the input DNA sequence
stl.header('INPUT (DNA QUERY)')
sequence

#DNA Nucleotide Count
stl.header('OUTPUT (DNA NUCLEOTIDE COUNT)')

#Print Dictionary
stl.subheader('1.Bases Dictionary')

def dna_nucleotide_count(seq):
    data_dict = dict([
        ('A',seq.count('A')),
        ('C',seq.count('C')),
        ('G',seq.count('G')),
        ('T',seq.count('T'))
    ])
    return data_dict

X = dna_nucleotide_count(sequence)
X

#Print Text
stl.subheader('2. Bases Text')
stl.write('There are  ' + str(X['A']) + ' adenine (A)')
stl.write('There are  ' + str(X['T']) + ' thymine (T)')
stl.write('There are  ' + str(X['G']) + ' guanine (G)')
stl.write('There are  ' + str(X['C']) + ' cytosine (C)')

#Display DataFrame
stl.subheader('3.Bases DataFrame')
df = pd.DataFrame.from_dict(X,orient='index')
df = df.rename({0:'Count'},axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index':'Nucleotide'})
stl.write(df)

#Display Bar Chart using Altair
stl.subheader('4.Bases BarChart')
chart = alt.Chart(df).mark_bar().encode(x='Nucleotide',y='Count')

chart = chart.properties(
    width=alt.Step(80)        #Controls Width of Bar
)
stl.write(chart)
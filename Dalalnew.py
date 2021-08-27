import streamlit as st
import pandas as pd
import base64
import io
from PIL import Image

#streamlit page configuration
st.set_page_config( layout="wide",page_title=None,page_icon=None)

#Streamlit Sidebar
image = Image.open('LOGO1.png')
st.sidebar.image(image)
txt = '<p style="font-family:georgia;text-align: center;color:black;font-weight: bold; font-size: 23px;">OSB Graduate Program</p>'
st.sidebar.markdown(txt, unsafe_allow_html=True)
st.sidebar.write("#")
st.sidebar.write("#")
txt = '<p style="font-family:georgia;text-align: center;color:black;font-weight: bold; font-size: 25px;">Open-Applications Processing Tool</p>'
st.sidebar.markdown(txt, unsafe_allow_html=True)
st.sidebar.write("#")
st.sidebar.write("#")
st.sidebar.write("#")
txt = '<p style="font-family:georgia;text-align: center;color:black; font-weight: bold;font-size: 20px;">Capstone Application prepared By Dalal El Khatib</p>'
st.sidebar.markdown(txt, unsafe_allow_html=True)
st.sidebar.write("#")
txt = '<p style="font-family:georgia;text-align: center;color:black; font-size: 15px;">Graduate Assistant at OSB Graduate Office</p>'
st.sidebar.markdown(txt, unsafe_allow_html=True)
txt = '<p style="font-family:georgia;text-align: center;color:black; font-size: 15px;">For further details contact : dme43@mail.aub.edu</p>'
st.sidebar.markdown(txt, unsafe_allow_html=True)
st.sidebar.write("#")
st.sidebar.write("#")
st.sidebar.write("#")
st.sidebar.write("#")
txt = '<p style="font-family:georgia;text-align: left;color:black;font-weight: bold; font-size: 20px;">Dashboard Password</p>'
st.sidebar.markdown(txt, unsafe_allow_html=True)
#password=st.sidebar.text_input("Please enter the password to access the Dashboard", value="", type="password")
password=st.sidebar.text_input("",value="", type="password")


def main():
    #st.title("Open-Applications Processing Tool")
    st.markdown("<h1 style='text-align: center;font-weight: bold;font-family:georgia;font-size: 40px; color:black;'>Open-Applications Processing Tool</h1>", unsafe_allow_html=True)
    st.write("#")
    st.write("#")
    st.markdown("<h1 style='text-align: Left;font-family:georgia; font-size: 30px;color:black;'>General Overview of Application</h1>", unsafe_allow_html=True)
    my_expander = st.beta_expander("GET TO KNOW MORE ABOUT THE APPLICATION", expanded=False)
    with my_expander:
        st.write("OSB Graduate office operates in a very dynamic environments that are constantly changing, whether that means records of new open application, accepted or enrolled. This flux of data produces serious operational challenges that must always be closely monitored. The goal is therefor to create a real-time dashboard that is automatically updated with the most recent relevant and immediate information.")
        st.write("The aim of this streamlit application is to process the weekly received report of Open-Applications as a first step of the plan the to be fed afterward into PowerBi for visualization.")
        image2 = Image.open('image1.png')
        st.image(image2)

    st.write("#")
    st.markdown("<h1 style='text-align: Left;font-family:georgia;font-size: 30px; color:black;'>Data Processing</h1>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: Left;font-family:georgia;font-size: 25px; color:black;'>1️⃣ Upload Last Week Updated CSV File  👇</h1>", unsafe_allow_html=True)


    @st.cache(allow_output_mutation=True)
    def load_data(file):
        df0 = pd.read_csv(file, encoding='latin-1')
        return df0

    uploaded_file = st.file_uploader("", type="csv", key='file_uploader')

    if uploaded_file is not None:
        df0 = load_data(uploaded_file)


    st.markdown("<h1 style='text-align: Left;font-family:georgia;font-size: 25px; color:black;'>2️⃣ Upload New CSV File Received From Admission Office👇</h1>", unsafe_allow_html=True)

    @st.cache(allow_output_mutation=True)
    def load_data(file):
        df1 = pd.read_csv(file, encoding='latin-1')
        return df1

    uploaded_file_2 = st.file_uploader("", type="csv", key='file_uploader_2')

    if uploaded_file_2 is not None:
        df1 = load_data(uploaded_file_2)

    if st.button("Let's Clean This Data"):
        #Drop Redundant Column
        df0=df0.drop(['Semester', 'Level','FacultyNames','R/T/S', 'Prefix','First Name',
           'Middle Name', 'Last Name','AUB ID','Phone Numbers','GRE Waiver',
           'Fee Waiver Requested', 'Fee Waivered', 'Share Contact Dtls', 'General Comments', 'IsLocked','PermState', 'PermCity', 'PermArea',
           'PermStreet', 'PermBuilding', 'PermPhone', 'PermCell',
           'CurrCountryRegions', 'CurrState', 'CurrCity', 'CurrArea', 'CurrStreet',
           'CurrBuilding', 'CurrPhone', 'CurrCell', 'Contacted By Phone',
           'Phone Contact Comments'], axis=1)
        #Spliting Programs by Priority
        # new data frame with split value columns
        new = df0["Programs"].str.split(",", n = 6, expand = True)
        #Merge 2 colums
        df0["Priority 1"] = new[0] + new[1]
        df0["Priority 2"] = new[2] + new[3]
        df0["Priority 3"] = new[4] + new[5]

        #Dropping old Programs columns
        df0.drop(columns =["Programs"], inplace = True)

        #Last Average
        # new data frame with split value columns
        new_gpa = df0["Latest Avg."].str.split("-", n = 1, expand = True)

        #making separate GPA column from new data frame
        df0["GPA"]= new_gpa[0]

        #Dropping old Last Avg. columns
        df0.drop(columns =["Latest Avg."], inplace = True)

        df0['Applicant Registration Date']= pd.to_datetime(df0['Applicant Registration Date'])
        df0['Application Creation Date']= pd.to_datetime(df0['Application Creation Date'])
        df0['Application Submission Date']= pd.to_datetime(df0['Application Submission Date'])

        #REPLACE "," BY "." and 'N/A,NA' BY ""
        df0['GPA']=df0['GPA'].str.replace(',', '.')
        df0['GPA']=df0['GPA'].str.replace('N/A', '')
        df0['GPA']=df0['GPA'].str.replace('NA', '')

        #cleaning the GPA column
        #Numeric GPA contains clean Numeric GPA , other NAN
        df0['Numeric GPA'] = df0['GPA'].str.extract('([0-9\.]+)', expand=False).str.strip()
        df0['Numeric GPA'] = pd.to_numeric(df0['Numeric GPA'],errors='coerce')

        #Letter GPA contains only String GPA , other NAN
        df0['Letter GPA'] = df0['GPA'].str.strip().str.extract('([a-zA-Z\+\s]+)', expand=False)

        #classifying students
        df0.loc[(df0['Universities'] == 'American University of Beirut (AUB)') & (df0['Numeric GPA'] >= 80), 'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'American University of Beirut (AUB)') & (df0['Numeric GPA'] < 80), 'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'American University of Beirut (AUB)') & (df0['Numeric GPA'] >= 3.2) & (df0['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'American University of Beirut (AUB)') & (df0['Numeric GPA'] < 3.2),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'UOB Balamand University') & (df0['Numeric GPA'] >= 80.9),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'UOB Balamand University') & (df0['Numeric GPA'] < 80.9),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'BAU Beirut Arab University') & (df0['Numeric GPA'] >= 80),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'BAU Beirut Arab University') & (df0['Numeric GPA'] < 80),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'BAU Beirut Arab University') & (df0['Numeric GPA'] >= 3.3) & (df0['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'BAU Beirut Arab University') & (df0['Numeric GPA'] < 3.3),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'Haigazian University') & (df0['Numeric GPA'] >= 80.4),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'Haigazian University') & (df0['Numeric GPA'] < 80.4),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'Lebanese American University (LAU)') & (df0['Numeric GPA'] >= 81.9),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'Lebanese American University (LAU)') & (df0['Numeric GPA'] < 81.9),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'Lebanese American University (LAU)') & (df0['Numeric GPA'] >= 3.5) & (df0['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'Lebanese American University (LAU)') & (df0['Numeric GPA'] < 3.5),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'Lebanese University (LU)') & (df0['Numeric GPA'] >= 66.7),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'Lebanese University (LU)') & (df0['Numeric GPA'] < 66.7),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'Lebanese University (LU)') & (df0['Numeric GPA'] >= 13.5),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'Lebanese University (LU)') & (df0['Numeric GPA'] < 13.5),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'Notre Dame University (NDU) - Louaize') & (df0['Numeric GPA'] >= 3.23)& (df0['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'Notre Dame University (NDU) - Louaize') & (df0['Numeric GPA'] < 3.23),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'USJ Université Saint-Joseph') & (df0['Numeric GPA'] >= 67.5),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'USJ Université Saint-Joseph') & (df0['Numeric GPA'] < 67.5),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'USJ Université Saint-Joseph') & (df0['Numeric GPA'] >= 13.6),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'USJ Université Saint-Joseph') & (df0['Numeric GPA'] < 13.6),'GPA_required'] = 'Mismatch'
        df0.loc[(df0['Universities'] == 'USEK Université Saint-Esprit de Kaslik') & (df0['Numeric GPA'] >= 85.9),'GPA_required'] = 'Match'
        df0.loc[(df0['Universities'] == 'USEK Université Saint-Esprit de Kaslik') & (df0['Numeric GPA'] < 85.9),'GPA_required'] = 'Mismatch'
        # st.write(df0)
        # towrite = io.BytesIO()
        # downloaded_file = df0.to_excel(towrite, encoding='utf-8', index=False, header=True)
        # towrite.seek(0)  # reset pointer
        # b64 = base64.b64encode(towrite.read()).decode()  # some strings
        # linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="df0.xlsx">Download excel file</a>'
        # st.markdown(linko, unsafe_allow_html=True)


        # if st.button("Let's Clean this data2"):
        #Drop Redundant Column
        df1=df1.drop(['Semester', 'Level','FacultyNames','R/T/S', 'Prefix','First Name',
           'Middle Name', 'Last Name','AUB ID','Phone Numbers','GRE Waiver',
           'Fee Waiver Requested', 'Fee Waivered', 'Share Contact Dtls', 'General Comments', 'IsLocked','PermState', 'PermCity', 'PermArea',
           'PermStreet', 'PermBuilding', 'PermPhone', 'PermCell',
           'CurrCountryRegions', 'CurrState', 'CurrCity', 'CurrArea', 'CurrStreet',
           'CurrBuilding', 'CurrPhone', 'CurrCell', 'Contacted By Phone',
           'Phone Contact Comments'], axis=1)


        #Spliting Programs by Priority
        # new data frame with split value columns
        new = df1["Programs"].str.split(",", n = 6, expand = True)

        #Merge 2 colums
        df1["Priority 1"] = new[0] + new[1]
        df1["Priority 2"] = new[2] + new[3]
        df1["Priority 3"] = new[4] + new[5]

        # Dropping old Programs columns
        df1.drop(columns =["Programs"], inplace = True)

        #Last Average

        # new data frame with split value columns
        new_gpa = df1["Latest Avg."].str.split("-", n = 1, expand = True)

        #making separate GPA column from new data frame
        df1["GPA"]= new_gpa[0]

        # Dropping old Last Avg. columns
        df1.drop(columns =["Latest Avg."], inplace = True)

        df1['Applicant Registration Date']= pd.to_datetime(df1['Applicant Registration Date'])
        df1['Application Creation Date']= pd.to_datetime(df1['Application Creation Date'])
        df1['Application Submission Date']= pd.to_datetime(df1['Application Submission Date'])

        #REPLACE "," BY "." and 'N/A,NA' BY ""
        df1['GPA']=df1['GPA'].str.replace(',', '.')
        df1['GPA']=df1['GPA'].str.replace('N/A', '')
        df1['GPA']=df1['GPA'].str.replace('NA', '')

        #cleaning the GPA column
        #Numeric GPA contains clean Numeric GPA , other NAN
        df1['Numeric GPA'] = df1['GPA'].str.extract('([0-9\.]+)', expand=False).str.strip()
        df1['Numeric GPA'] = pd.to_numeric(df1['Numeric GPA'],errors='coerce')

        #Letter GPA contains only String GPA , other NAN
        df1['Letter GPA'] = df1['GPA'].str.strip().str.extract('([a-zA-Z\+\s]+)', expand=False)

        #Set Index for Merge Purposes
        #df0.set_index('Application Code', inplace=True)
        #df1.set_index('Application Code', inplace=True)


        for index, row in df1.iterrows():
            if( index in df0.index.values):
                df1.loc[index, "Category"] = 'Returning'
                df1.loc[index, "Old %"] = df0.loc[index,"% Complete"]

                if(df1.loc[index, 'Admission Submission Status']=='Submitted' and df0.loc[index, 'Admission Submission Status']=='Pending'):
                    df1.loc[index, 'Newly Sub'] = True
                else:
                    df1.loc[index, 'Newly Sub'] = False
            else:
                df1.loc[index, "Category"] = 'New'

        df1['Comment'] = ""

        #Status of completion
        df1['% Complete'] = df1['% Complete'].str.rstrip('%').astype('float') / 100.0
        df1['Old %'] = df1['Old %'].str.rstrip('%').astype('float') / 100.0


        #st.markdown(df1['% Complete'].dtypes)
        #st.markdown(df1['Old %'].dtypes)
        df1['Difference of Completion'] = df1['% Complete'] - df1['Old %']
        df1.loc[(df1['Difference of Completion'] <= 0.2), 'Status  of completetion '] = 'Slow'
        df1.loc[(df1['Difference of Completion'] > 0.2) & (df1['Difference of Completion'] <= 0.6), 'Status  of completetion '] = 'Medium'
        df1.loc[(df1['Difference of Completion'] >= 0.6), 'Status  of completetion '] = 'Very Interested'
        #
        #
        #Submission SPAN
        df1['Applicant Registration Date']= pd.to_datetime(df1['Applicant Registration Date'])
        df1['Application Creation Date']= pd.to_datetime(df1['Application Creation Date'])
        df1['Application Submission Date']= pd.to_datetime(df1['Application Submission Date'])

        df1['Submission Span'] = (df1['Application Submission Date'] - df1['Application Creation Date']).dt.days

        #Time SPAN
        df1['Time Span'] = (df1['Application Submission Date'] - df1['Applicant Registration Date']).dt.days


        #classifying students
        df1.loc[(df1['Universities'] == 'American University of Beirut (AUB)') & (df1['Numeric GPA'] >= 80), 'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'American University of Beirut (AUB)') & (df1['Numeric GPA'] < 80), 'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'American University of Beirut (AUB)') & (df1['Numeric GPA'] >= 3.2) & (df1['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'American University of Beirut (AUB)') & (df1['Numeric GPA'] < 3.2),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'UOB Balamand University') & (df1['Numeric GPA'] >= 80.9),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'UOB Balamand University') & (df1['Numeric GPA'] < 80.9),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'BAU Beirut Arab University') & (df1['Numeric GPA'] >= 80),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'BAU Beirut Arab University') & (df1['Numeric GPA'] < 80),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'BAU Beirut Arab University') & (df1['Numeric GPA'] >= 3.3) & (df1['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'BAU Beirut Arab University') & (df1['Numeric GPA'] < 3.3),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'Haigazian University') & (df1['Numeric GPA'] >= 80.4),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'Haigazian University') & (df1['Numeric GPA'] < 80.4),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'Lebanese American University (LAU)') & (df1['Numeric GPA'] >= 81.9),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'Lebanese American University (LAU)') & (df1['Numeric GPA'] < 81.9),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'Lebanese American University (LAU)') & (df1['Numeric GPA'] >= 3.5) & (df1['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'Lebanese American University (LAU)') & (df1['Numeric GPA'] < 3.5),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'Lebanese University (LU)') & (df1['Numeric GPA'] >= 66.7),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'Lebanese University (LU)') & (df1['Numeric GPA'] < 66.7),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'Lebanese University (LU)') & (df1['Numeric GPA'] >= 13.5),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'Lebanese University (LU)') & (df1['Numeric GPA'] < 13.5),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'Notre Dame University (NDU) - Louaize') & (df1['Numeric GPA'] >= 3.23)& (df1['Numeric GPA']< 5),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'Notre Dame University (NDU) - Louaize') & (df1['Numeric GPA'] < 3.23),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'USJ Université Saint-Joseph') & (df1['Numeric GPA'] >= 67.5),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'USJ Université Saint-Joseph') & (df1['Numeric GPA'] < 67.5),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'USJ Université Saint-Joseph') & (df1['Numeric GPA'] >= 13.6),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'USJ Université Saint-Joseph') & (df1['Numeric GPA'] < 13.6),'GPA_required'] = 'Mismatch'
        df1.loc[(df1['Universities'] == 'USEK Université Saint-Esprit de Kaslik') & (df1['Numeric GPA'] >= 85.9),'GPA_required'] = 'Match'
        df1.loc[(df1['Universities'] == 'USEK Université Saint-Esprit de Kaslik') & (df1['Numeric GPA'] < 85.9),'GPA_required'] = 'Mismatch'

        st.write(df1)
        towrite = io.BytesIO()
        downloaded_file = df1.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()  # some strings

        linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="df1.xlsx">Download Updated Excel File</a>'

        st.markdown(linko, unsafe_allow_html=True)

if password=='aubosb':
    main()
#elif password !='aubosb':
        #st.error("Authentication failed. Please verify your password and try again. ")
        #txt = '<p style="font-family:georgia;text-align: left;color:black; font-weight: bold;font-size: 10px;">Authentication failed. Please verify your password and try again.</p>'
        #st.sidebar.markdown(txt, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

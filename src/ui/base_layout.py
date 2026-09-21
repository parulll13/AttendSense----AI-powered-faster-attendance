import streamlit as st

#BACKGROUND COLOUR FOR HOMESCREEN
def style_background_home():
    st.markdown("""
        <style>
            .stApp{
                Background: white !important;
                }
            .stApp div[data-testid="stColumn"]{
                background-color: white !important;
                border-radius: 3rem !important;
                padding: 10px 10px 10px 10px;

                /* Center contents vertically and horizontally */
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
            }   

            /* Center header text inside columns */
            [data-testid="stColumn"] h2 {
                text-align: center;
                margin-bottom: 15px;
            }

            /* Optional: ensure images and buttons inside the column center align properly */
                .stApp div[data-testid="stColumn"] > div {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%;
                }

        </style>
        """
        ,unsafe_allow_html=True)


#BACKGROUND COLOUR FOR OTHER SCREENS
def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp{
                Background: #E0E3FF !important;
                }
        </style>
        """
        ,unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&display=swap');
       
        
        h1{
            font-family: 'Lobster Two', sans-serif  !important;
            font-size: 3rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            margin-top: 0rem !important;
        }

        h2{
            font-family: 'Lobster Two', sans-serif !important;
            font-size: 2rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }

        h3, h4, p{
            font-family: 'Source Serif 4', sans-serif !important;
        }

        button[kind ="primary"]{
            border-radius: 1.5rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transistion: transform 0.25s ease-in-out !important;
        }

        button[kind ="secondary"]{
            border-radius: 1.5rem !important;
            background-color: #EB459E !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transistion: transform 0.25s ease-in-out !important;
        }

        button[kind ="tertiary"]{
            border-radius: 1.5rem !important;
            background-color: black !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transistion: transform 0.25s ease-in-out !important;
        }

        button:hover{
            transform:scale(1.05)
        }

        /* Hide Top Bar Of streamlit */
            #MainMenu, footer, header{
                visibility: hidden
            }
            .block-container{
                padding-top:0.6rem !important;
            }
        
        </style>
        """
        ,unsafe_allow_html=True)
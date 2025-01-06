import streamlit as st 
import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt
import base64
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(layout='wide')

# Define notes file path
notes_file_path = "notes.txt"

data = pd.read_csv('./data/GAST-GT-08-31-24-PLAYS')

#region functions

# Read notes from the file
def load_notes(file_path):
    try:
        with open(file_path, "r") as file:
            notes = file.readlines()
            return [note.strip() for note in notes]
    except FileNotFoundError:
        return ["Notes file not found. Please check the file path."]

def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def create_circular_progress_bar(percentage, title_input, color_input):
    # Ensure a fresh figure every time
    fig = go.Figure()

    # Determine the color based on input
    color = '#0afa46' if color_input == 'green' else (
        '#2499ff' if color_input == 'blue' else '#e38c00'
    )


    # Add a full circle for the background
    fig.add_trace(go.Pie(
        values=[1],
        hole=0.7,
        marker_colors=['#e6e5e3'],
        showlegend=False,
        textinfo='none'
    ))

    # Add a partial circle for the progress
    fig.add_trace(go.Pie(
        values=[percentage/100, (1-(percentage/100))],  # Correctly map progress and remainder
        hole=0.7,
        marker=dict(
            colors=[color, 'rgba(0,0,0,0)'],  # Progress color and transparent remainder
            line=dict(color='black', width=1)  # Black outline
        ),
        direction='counterclockwise',
        rotation=0,  # Start from the top of the circle
        showlegend=False,
        textinfo='none'
    ))

    # Update layout to make the background transparent and add a title
    fig.update_layout(
        title={
            'text': f"{title_input}: {percentage}%",
            'y': 0.95,  # Position the title closer to the top
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'color': 'gray',  # Gray color for the title
                'size': 12        # Smaller font size
            }
        },
        margin=dict(t=20, b=5, l=0, r=0),
        width=100,  # Adjust size for better alignment
        height=100,
        paper_bgcolor="rgba(0,0,0,0)"  # Transparent background
    )

    return fig

dummy_pie = create_circular_progress_bar(100,'dummy','green')

#endregion

header = st.container()
header_cols = header.columns(6)

notes = load_notes(notes_file_path)
with header_cols[0].popover('Notes', use_container_width=True):
    for note in notes:
        st.warning('* '+note)

                
editor_exp = st.expander('editor')
dashboard_container = st.container()
off_playbook_exp = st.expander('offensive review')
player_eval_exp = st.expander('offensive player eval')
player_yot_exp = st.expander('offensive player yards over time')

#region editor
    

# with editor_exp:
#     columns = ['down', 'ytg', 'field_pos', 'player', 'action', 'completed', 'yds']
#     df = pd.DataFrame(columns=columns)
#     cols = st.columns([0.1,0.4,0.2,0.3])
#     with cols[1]:
#         editor_df_container = st.empty()
#         dynamic_df = editor_df_container.data_editor(df, num_rows="dynamic")
#     with cols[2]:
#         title = st.text_input('Title')
#         save_button = st.button('Save')
#         if save_button:
#             dynamic_df.to_csv('./data/'+title, index=False)
#             st.rerun()

#endregion


#region overall_off

with dashboard_container:
    cols = st.columns([0.5,0.5])
    df = data.copy()
    # Determine Pass / Rush Ratio
    plays = len(df)
    passing_df = df[df['action']=='rec']
    rushing_df = df[df['action']=='rush']
    # plays == len(passing_df)+len(rushing_df)
    p_ratio = (len(passing_df)/plays)*100
    r_ratio = (len(rushing_df)/plays)*100
    # Avg Yds per Rec
    p_avg = passing_df['yds'].mean()
    # Avg Yds per Carry
    r_avg = rushing_df['yds'].mean()
    # Completion %
    comp_df = passing_df[passing_df['completed']==True]
    comp_pct = len(comp_df)/len(passing_df)
    # Effective Carry %
    eff_car_df = rushing_df[(rushing_df['yds']>5.0) | (rushing_df['converted']==True)]
    eff_car_pct = len(eff_car_df)/len(rushing_df)
    
    with cols[0]:
        with stylable_container(
            key="container_with_border_black",
            css_styles="""
                {
                    border: 1px solid rgba(100, 100, 100, 0.5);
                    border-radius: 0.5rem;
                    padding: 1px;
                }
                """,
        ):
            plays_container_cols = st.columns([0.04,0.92,0.04])
            with plays_container_cols[1]:
                add_vertical_space(2)
                st.dataframe(df,use_container_width=True)
                add_vertical_space(1)
    
    with cols[1]:
        with stylable_container(
            key="container_with_border_black",
            css_styles="""
                {
                    border: 1px solid rgba(100, 100, 100, 0.5);
                    border-radius: 0.5rem;
                    padding: 20px;
                }
                """,
        ):
            add_vertical_space(4)
            metric_container_cols = st.columns([0.06,0.22,0.22,0.22,0.22,0.06])
            plays_total =    metric_container_cols[1].metric(label='Plays',value=plays,delta=9)
            drives =         metric_container_cols[2].metric(label='Drives',value=10,delta=3)
            scoring_drives = metric_container_cols[3].metric(label='Scoring Drives',value=5,delta=1)
            points =         metric_container_cols[4].metric(label='Points',value=35,delta=9)
            pass_pct =       metric_container_cols[1].metric(label='Pass %',value=round(p_ratio,1),delta=16.7)
            pass_avg =       metric_container_cols[2].metric(label="Avg Rec Yds / Att", value=round(p_avg,1), delta=0.3)
            pass_cmp =       metric_container_cols[3].metric(label='Completion %',value=round(comp_pct,2)*100,delta=17)
            pass_total =     metric_container_cols[4].metric(label='Total Passing (yds)',value=(round(passing_df['yds'].sum(),2)),delta=128)
            rush_pct =       metric_container_cols[1].metric(label='Rush %',value=round(r_ratio,1),delta=-16.7)
            rush_avg =       metric_container_cols[2].metric(label="Avg Rush Yds / Att", value=round(r_avg,1), delta=1.6)
            rush_eff =       metric_container_cols[3].metric(label='Rush Efficacy',value=round(eff_car_pct,2),delta=-0.17)
            rush_total =     metric_container_cols[4].metric(label='Total Rushing (yds)',value=(round(rushing_df['yds'].sum(),2)),delta=30)
            style_metric_cards()
            add_vertical_space(1)

#endregion


#region off_playbook

with off_playbook_exp:        
    gt_terr_container = st.container()
    st.divider()
    opp_terr_container = st.container()
    st.divider()
    red_zone_container = st.container()
    df = data.copy()

    with gt_terr_container:
        gt_terr_first_container = st.container()
        gt_terr_third_container = st.container()
        cols_first = gt_terr_first_container.columns(2)
        cols_third = gt_terr_third_container.columns(2)
        with cols_first[0]:
            df_gt_terr = df[df['field_pos']<50]
            df_gt_terr_first = df_gt_terr[df_gt_terr['down']==1]
            df_gt_terr_first = df_gt_terr_first.sort_values(['action','yds'],ascending=True)
            st.table(df_gt_terr_first)
        with cols_first[1]:
            add_vertical_space(1)
            st.success('7/7 passes completed (100%) on 1st down in GT territory')
            st.warning('10/17 efficient movements (58.8%) of the ball on 1st down in GT territory. Aiming for 60-65% ... especially vs 112th total defense GAST.')
            st.error('3/8 effective carries (37.5%) on 1st down in GT territory. Again too low vs T123rd rushing defense.')
            st.error('3/17 conversions (17.6%) on 1st down in GT territory.')
        with cols_third[0]:
            df_gt_terr_third = df_gt_terr[df_gt_terr['down']==3]
            df_gt_terr_third = df_gt_terr_third.sort_values(['action','yds'],ascending=True)
            st.table(df_gt_terr_third)
        with cols_third[1]:
            add_vertical_space(1)
            st.success('2/2 efficient carries (100%) on 3rd down in GT territory')
            st.success('3/5 conversions (60%) on 3rd down in GT territory')
         
         
    with opp_terr_container:   
        opp_terr_first_container = st.container()
        opp_terr_third_container = st.container()
        cols_first = opp_terr_first_container.columns(2)
        cols_third = opp_terr_third_container.columns(2)
        with cols_first[0]:
            df_opp_terr = df[(df['field_pos']>=50)&(df['field_pos']<80)]
            df_opp_terr_first = df_opp_terr[df_opp_terr['down']==1]
            df_opp_terr_first = df_opp_terr_first.sort_values(['action','yds'],ascending=True)
            st.table(df_opp_terr_first)
        with cols_first[1]:    
            add_vertical_space(1)
            st.warning('3/8 conversions (37.5%) on 1st down in between midfield and the red zone.')
            st.error('3/8 efficient movements (37.5%) of the ball on 1st down in between midfield and the red zone. ')
        with cols_third[0]:  
            df_opp_terr_third = df_opp_terr[df_opp_terr['down']==3]
            df_opp_terr_third = df_opp_terr_third.sort_values(['action','yds'],ascending=True)
            st.table(df_opp_terr_third)
        with cols_third[1]:
            add_vertical_space(1)
            st.success('1/2 conversions (50%) on 3rd down in between midfield and the redzone.')
    
    with red_zone_container:
        red_zone_first_container = st.container()
        red_zone_third_container = st.container()
        cols_first = red_zone_first_container.columns(2)
        cols_third = red_zone_third_container.columns(2)
 
        with cols_first[0]:
            df_red_zone = df[df['field_pos']>=80]
            df_red_zone_first = df_red_zone[df_red_zone['down']==1]
            df_red_zone_first = df_red_zone_first.sort_values(['action','yds'],ascending=True)
            st.table(df_red_zone_first)
        with cols_first[1]:
            add_vertical_space(1)
            st.error('0/4 efficient movements (0%) of the ball on 1st down in the redzone.')
            st.error('0/4 conversions (0%) on 1st down in the redzone.')
        with cols_third[0]:    
            df_red_zone_third = df_red_zone[df_red_zone['down']==3]
            df_red_zone_third = df_red_zone_third.sort_values(['action','yds'],ascending=True)
            st.table(df_red_zone_third)
        with cols_third[1]:
            st.success('1/2 efficient movements (50%) of the ball on 3rd down in the redzone.')
            st.error('0/2 conversions (0%) on 3rd down in the redzone.')
        
        
        
#endregion


# #region player_eval
           
# with player_eval_exp:
#     cols = st.columns([0.05,0.3,0.3,0.3,0.05])
#     results = {}
#     passing_df = df[df['action']=='rec']
#     rushing_df = df[df['action']=='rush']
#     skill_players_rec = passing_df['player'].unique().tolist()
#     skill_players_rush = rushing_df['player'].unique().tolist()
#     #QB edge case
#     results['king'] = {'plays':0,'att':0,'cmp':0,'pass_yds':0,
#                                'targets':0, 'rec':0, 'rec_yds':0, 'car':0,
#                                'eff_car':0, 'rush_yds':0}
#     for player in skill_players_rec:
#         if player not in results.keys():
#             results[player] = {'plays':0,'att':0,'cmp':0,'pass_yds':0,
#                                'targets':0, 'rec':0, 'rec_yds':0, 'car':0,
#                                'eff_car':0, 'rush_yds':0}
#         df_player = df[df['player']==player]   
#         df_player_rec = df_player[df_player['action']=='rec']
#         # Plays     
#         results[player]['plays'] = len(df_player_rec)
#         # Cmp 
#         results[player]['targets'] = len(df_player_rec)
#         df_player_cmp = df_player_rec[df_player_rec['completed']==True]
#         results[player]['rec'] = len(df_player_cmp)
#         results['king']['cmp'] += len(df_player_cmp)
#         # Yds
#         rec_yds = df_player_cmp['yds'].sum()
#         results[player]['rec_yds'] = rec_yds
#     results['king']['pass_yds'] = passing_df['yds'].sum()
#     results['king']['att'] = len(passing_df)
#     results['king']['plays'] = len(passing_df)
#     for player in skill_players_rush:
#         if player not in results.keys():
#             results[player] = {'plays':0,'att':0,'cmp':0,'pass_yds':0,
#                                'targets':0, 'rec':0, 'rec_yds':0, 'car':0,
#                                'eff_car':0, 'rush_yds':0}
#         df_player = df[df['player']==player]   
#         df_player_rush = df_player[df_player['action']=='rush']
#         # Plays    
#         if 'plays' not in results[player].keys(): 
#             results[player]['plays'] = len(df_player_rush)
#         else:
#             results[player]['plays'] += len(df_player_rush)
#         # Effective Carries
#         results[player]['car'] = len(df_player_rush)
#         df_player_eff = df_player_rush[(df_player_rush['yds']>5.0) | (df_player_rush['converted']==True)]
#         results[player]['eff_car'] = len(df_player_eff)
#         # Yds
#         rush_yds = df_player_rush['yds'].sum()
#         results[player]['rush_yds'] = rush_yds
       
#     sorted_data = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['plays'], reverse=True)}

#     for i,player in enumerate(sorted_data):  
#         with cols[(i%3)+1]:  
#             with stylable_container(
#                 key=f"container_with_border_{player}",
#                 css_styles="""
#                     {
#                         border: 2px solid rgba(100, 100, 100, 0.5);
#                         border-radius: 0.5rem;
#                         padding: calc(1em - 1px)
                        
#                     }
#                     """,
#                 ):
#                 st.markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>{player}</p>", unsafe_allow_html=True)
#                 image = "./pics/"+player+".jpg"
#                 base64_image = get_image_as_base64(image)
#                 markdown_str = f"""<div style="text-align:center;"><img src="data:image/jpeg;base64,{base64_image}" alt="{player}" width="250" style="border-radius:10px;"></div>"""
#                 st.markdown(markdown_str, unsafe_allow_html=True)
#                 container_cols = st.columns([0.05,0.5,0.4,0.05])
#                 with container_cols[1]:
#                     add_vertical_space(1)
#                     st.write(sorted_data[player])
#                 with container_cols[2]:
#                     add_vertical_space(2)
#                     if player != 'king':
#                         if sorted_data[player]['targets'] > 0:
#                             cmp_pct = round((sorted_data[player]['rec']/sorted_data[player]['targets'])*100,2)
#                             fig = create_circular_progress_bar(cmp_pct, 'rec_eff','green')
#                             st.plotly_chart(fig,use_container_width=True,key=player+'cmp')
#                         if sorted_data[player]['car'] > 0:
#                             eff_car_pct = round((sorted_data[player]['eff_car']/sorted_data[player]['car'])*100,2)
#                             fig = create_circular_progress_bar(eff_car_pct, 'car_eff', 'blue')
#                             st.plotly_chart(fig,use_container_width=True,key=player+'eff')
#                     else:
#                         if sorted_data[player]['att'] > 0:
#                             cmp_pct = round((sorted_data[player]['cmp']/sorted_data[player]['att'])*100,2)
#                             fig = create_circular_progress_bar(cmp_pct, 'cmp','orange')
#                             st.plotly_chart(fig,use_container_width=True,key=player+'cmp')
#                         if sorted_data[player]['car'] > 0:
#                             eff_car_pct = round((sorted_data[player]['eff_car']/sorted_data[player]['car'])*100,2)
#                             fig = create_circular_progress_bar(100-eff_car_pct, 'car_eff', 'blue')
#                             st.plotly_chart(fig,use_container_width=True,key=player+'eff')
                    
#     #endregion
    
# #region player_yot           
# with player_yot_exp:
#     top = st.container()
#     mid = st.container()
#     bot = st.container()
#     top_cols = top.columns([0.05,0.3,0.3,0.3,0.05])
#     mid_cols = mid.columns([0.05,0.3,0.3,0.3,0.05])
#     bot_cols = bot.columns([0.05,0.3,0.3,0.3,0.05])
#     df = pd.read_csv('./data/FSU-GT-08-24-24-PLAYS')
#     skill_players = df['player'].unique().tolist()
#     i = -1
#     top_cols[1].success('consistent! efficient movements of the ball agnostic of game clock.')
#     top_cols[2].warning('low production but dependable target.')
#     top_cols[3].warning('potentially detrimental incompletions. productive in clutch time.')
#     for player in skill_players:
#         i += 1
#         df_player = df[df['player']==player]  
#         if len(df_player) < 3:
#             i -= 1
#             continue
#         with mid_cols[(i%3)+1]:
#             # Create a new figure for each player
#             fig, ax = plt.subplots()
#             # Plot yards vs. index for the current player (using index as x-axis)
#             ax.plot(df_player.index, df_player['yds'], marker='o', label=player)
#             if player == 'king':
#                 df_rec = df[df['action']=='rec']
#                 ax.plot(df_rec.index, df_rec['yds'], marker='o', label=player+' passing')
#             # Label the axes and title
#             ax.set_xlabel('Play')
#             ax.set_ylabel('Yards (yds)')
#             ax.set_title('yds over time')
#             # Add a legend
#             ax.legend()
#             # Display the plot in Streamlit
#             st.pyplot(fig)
#     bot_cols[1].success('great balance for our offense.')
#     bot_cols[2].success('RB2!')

                
            
# #endregion    


# st.warning('Defensive Analysis work in progress... Will begin to populate expanders when finished with offensive review of each game.')

# defensive_review_exp = st.expander('defensive review')
# def_eval_exp = st.expander('defensive player eval')

# #region TO DO

# with defensive_review_exp:
#     st.write('work in progress')
    
# with def_eval_exp:
#     st.write('work in progress')

# #endregion
          
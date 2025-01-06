import streamlit as st 
import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt
import base64
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(layout='wide')
folder_path = "./data"
data = pd.read_csv('./data/FSU-GT-08-24-24-PLAYS')

#region functions

def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def create_circular_progress_bar(percentage, title_input, color_input):
    # Create a figure
    fig = go.Figure()
    if color_input == 'green':
        color = '#0afa46'
    if color_input == 'blue':
        color = '#2104d9'
    if color_input == 'orange':
        color = '#e38c00'

    # Add a full circle for the background
    fig.add_trace(go.Pie(
        values=[1],
        hole=0.7,
        marker_colors=['#3f403f', 'rgba(0,0,0,0)'],  # Grey and transparent
        showlegend=False,
        textinfo='none'
    ))

    # Add a partial circle for the progress
    fig.add_trace(go.Pie(
        values=[percentage, 100 - percentage],
        hole=0.7,
        marker_colors=[color, 'rgba(0,0,0,0)'],  # Green and transparent
        direction='counterclockwise',
        rotation=0,  # Start from the top
        showlegend=False,
        textinfo='none'
    ))

    # Update layout to make the background transparent
    fig.update_layout(
        title={
            'text': f"{title_input} : {percentage}%",
            'y': 0.9999,  # Position the title closer to the top
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
            'color': 'gray',  # Gray color for the title
            'size': 16        # Slightly smaller font size
        }
        },
        margin=dict(t=20, b=0, l=0, r=0),
        width=75,
        height=75,
        paper_bgcolor="rgba(0,0,0,0)"  # Transparent background
    )

    return fig

#endregion

# Get all file names in the folder
file_names = os.listdir(folder_path)

with st.sidebar:
    st.warning('* For the most part, graphs will only be generated for players with 3 or more data points to pull from.')
    st.warning('* Any Loss/Gain of Yardage on offense not due to passing or penalty is counted in each rushing related stat.')
    st.warning('* Rush Efficacy describes the ratio of efficient carries to overall attempts.')  
    st.warning('* Efficient movements of the ball describe plays that advance the ball >= 5 yards or convert.')
    st.warning('* Return Yardage is not yet being tracked.')
    st.warning('* Defensive analysis in the works for future reviews.')

editor_exp = st.expander('editor')
overall_off_exp = st.expander('overall offense review')
off_playbook_exp = st.expander('offensive playbook')
player_eval_exp = st.expander('individual player eval')
player_yot_exp = st.expander('individual player yards over time')

#region editor

# with st.sidebar:
#     user = st.text_input('user')
#     password = st.text_input('pass')
    
# if user == 'admin':
#     if password == 'admin':
# with editor_exp:
#     columns = ['opp','player', 'down', 'ytg', 'action','completed', 'yds']
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
with overall_off_exp:
    top =st.container()
    bot = st.container()
    with top:
        cols = st.columns([0.1,0.4,0.1,0.1,0.1,0.1,0.1])
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
        for i,col in enumerate(cols):
            if i < 2:
                continue
            with col:
                add_vertical_space(2)
        with cols[1]:
            st.dataframe(df)
        plays_total = cols[2].metric(label='Plays',value=plays,delta=0)
        drives = cols[3].metric(label='Drives',value=7,delta=0)
        scoring_drives = cols[4].metric(label='Scoring Drives',value=4,delta=0)
        points = cols[5].metric(label='Points',value=24,delta=0)
        pass_pct = cols[2].metric(label='Pass %',value=round(p_ratio,1),delta=0)
        pass_avg = cols[3].metric(label="Avg Rec Yds / Att", value=round(p_avg,1), delta=0)
        pass_cmp = cols[4].metric(label='Completion %',value=round(comp_pct,2)*100,delta=0)
        pass_total = cols[5].metric(label='Total Passing (yds)',value=(round(passing_df['yds'].sum(),2)),delta=0)
        rush_pct = cols[2].metric(label='Rush %',value=round(r_ratio,1),delta=0)
        rush_avg = cols[3].metric(label="Avg Rush Yds / Att", value=round(r_avg,1), delta=0)
        rush_eff = cols[4].metric(label='Rush Efficacy',value=round(eff_car_pct,2),delta=0)
        rush_total = cols[5].metric(label='Total Rushing (yds)',value=(round(rushing_df['yds'].sum(),2)),delta=0)

    with bot:
        cols = st.columns([0.45,0.45,0.1])
#endregion

#region off_playbook

with off_playbook_exp:
    gt_terr_container = st.container()
    st.divider()
    opp_terr_container = st.container()
    st.divider()
    red_zone_container = st.container()
    cols = gt_terr_container.columns([0.5,0.25,0.25])
    with cols[0]:
        df = data.copy()
        df_gt_terr = df[df['field_pos']<50]
        df_gt_terr_first = df_gt_terr[df_gt_terr['down']==1]
        df_gt_terr_first = df_gt_terr_first.sort_values(['action','yds'],ascending=True)
        st.table(df_gt_terr_first)
        df_gt_terr_third = df_gt_terr[df_gt_terr['down']==3]
        df_gt_terr_third = df_gt_terr_third.sort_values(['action','yds'],ascending=True)
        st.table(df_gt_terr_third)
    with cols[1]:
        add_vertical_space(3)
        st.success('4/5 passes completed (80%) on 1st down in GT territory')
        st.success('5/8 effective carries (62.5%) on 1st down in GT territory')
        st.success('8/13 efficient movements (61.5%) of the ball on 1st down in GT territory.')
        st.error('5/13 conversions (38.5%) on 1st down in GT territory. Should be > 40% with our Pass/Rush Ratio and efficacy.')
        add_vertical_space(12)
        st.success('2/4 conversions (50%) on 3rd down in GT territory')
    cols = opp_terr_container.columns([0.5,0.25,0.25])
    with cols[0]:
        df_opp_terr = df[(df['field_pos']>=50)&(df['field_pos']<80)]
        df_opp_terr_first = df_opp_terr[df_opp_terr['down']==1]
        df_opp_terr_first = df_opp_terr_first.sort_values(['action','yds'],ascending=True)
        st.table(df_opp_terr_first)
        df_opp_terr_third = df_opp_terr[df_opp_terr['down']==3]
        df_opp_terr_third = df_opp_terr_third.sort_values(['action','yds'],ascending=True)
        st.table(df_opp_terr_third)
    with cols[1]:
        add_vertical_space(3)
        st.warning('3/7 efficient movements (42.9%) of the ball on 1st down in between midfield and the red zone. ')
        st.error('0/7 conversions (0%) on 1st down in between midfield and the red zone.')
        add_vertical_space(8)
        st.success('3/4 efficient movements (75%) of the ball on 3rd down in between midfield and the redzone.')
    cols = red_zone_container.columns([0.5,0.25,0.25])
    with cols[0]:
        df_red_zone = df[df['field_pos']>=80]
        df_red_zone_first = df_red_zone[df_red_zone['down']==1]
        df_red_zone_first = df_red_zone_first.sort_values(['action','yds'],ascending=True)
        st.table(df_red_zone_first)
        df_red_zone_third = df_red_zone[df_red_zone['down']==3]
        df_red_zone_third = df_red_zone_third.sort_values(['action','yds'],ascending=True)
        st.table(df_red_zone_third)
    with cols[1]:
        add_vertical_space(3)
        st.success('3/6 efficient movements (50%) of the ball on 1st down in the redzone.')
        st.warning('0 passes in 6 redzone 1st downs.')
        add_vertical_space(6)
        st.success('3rd and goal.... hand it off to Jamal.')
        
        
#endregion

#region player_eval
           
with player_eval_exp:
    cols = st.columns([0.05,0.3,0.3,0.3,0.05])
    results = {}
    passing_df = df[df['action']=='rec']
    rushing_df = df[df['action']=='rush']
    skill_players_rec = passing_df['player'].unique().tolist()
    skill_players_rush = rushing_df['player'].unique().tolist()
    #QB edge case
    results['king'] = {'plays':0,'att':0,'cmp':0,'pass_yds':0,
                               'targets':0, 'rec':0, 'rec_yds':0, 'car':0,
                               'eff_car':0, 'rush_yds':0}
    for player in skill_players_rec:
        if player not in results.keys():
            results[player] = {'plays':0,'att':0,'cmp':0,'pass_yds':0,
                               'targets':0, 'rec':0, 'rec_yds':0, 'car':0,
                               'eff_car':0, 'rush_yds':0}
        df_player = df[df['player']==player]   
        df_player_rec = df_player[df_player['action']=='rec']
        # Plays     
        results[player]['plays'] = len(df_player_rec)
        # Cmp 
        results[player]['targets'] = len(df_player_rec)
        df_player_cmp = df_player_rec[df_player_rec['completed']==True]
        results[player]['rec'] = len(df_player_cmp)
        results['king']['cmp'] += len(df_player_cmp)
        # Yds
        rec_yds = df_player_cmp['yds'].sum()
        results[player]['rec_yds'] = rec_yds
    results['king']['pass_yds'] = passing_df['yds'].sum()
    results['king']['att'] = len(passing_df)
    results['king']['plays'] = len(passing_df)
    for player in skill_players_rush:
        if player not in results.keys():
            results[player] = {'plays':0,'att':0,'cmp':0,'pass_yds':0,
                               'targets':0, 'rec':0, 'rec_yds':0, 'car':0,
                               'eff_car':0, 'rush_yds':0}
        df_player = df[df['player']==player]   
        df_player_rush = df_player[df_player['action']=='rush']
        # Plays    
        if 'plays' not in results[player].keys(): 
            results[player]['plays'] = len(df_player_rush)
        else:
            results[player]['plays'] += len(df_player_rush)
        # Effective Carries
        results[player]['car'] = len(df_player_rush)
        df_player_eff = df_player_rush[(df_player_rush['yds']>5.0) | (df_player_rush['converted']==True)]
        results[player]['eff_car'] = len(df_player_eff)
        # Yds
        rush_yds = df_player_rush['yds'].sum()
        results[player]['rush_yds'] = rush_yds
       
    sorted_data = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['plays'], reverse=True)}
    for i,player in enumerate(sorted_data):  
        with cols[(i%3)+1]:  
            with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 3px solid rgba(255, 255, 255, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px)
                        
                    }
                    """,
                ):
                st.markdown(f"<p style='text-align: center; color: white; font-size: 14px;'>{player}</p>", unsafe_allow_html=True)
                image = "./pics/"+player+".jpg"
                base64_image = get_image_as_base64(image)
                markdown_str = f"""<div style="text-align:center;"><img src="data:image/jpeg;base64,{base64_image}" alt="{player}" width="300" style="border-radius:10px;"></div>"""
                st.markdown(markdown_str, unsafe_allow_html=True)
                container_cols = st.columns([0.05,0.5,0.4,0.05])
                with container_cols[1]:
                    st.write(sorted_data[player])
                with container_cols[2]:
                    add_vertical_space(2)
                    if player != 'king':
                        if sorted_data[player]['targets'] > 0:
                            cmp_pct = round((sorted_data[player]['rec']/sorted_data[player]['targets'])*100,2)
                            fig = create_circular_progress_bar(cmp_pct, 'rec_eff','green')
                            st.plotly_chart(fig,use_container_width=True)
                    else:
                        if sorted_data[player]['att'] > 0:
                            cmp_pct = round((sorted_data[player]['cmp']/sorted_data[player]['att'])*100,2)
                            fig = create_circular_progress_bar(cmp_pct, 'cmp','orange')
                            st.plotly_chart(fig,use_container_width=True)
                    if sorted_data[player]['car'] > 0:
                        eff_car_pct = round((sorted_data[player]['eff_car']/sorted_data[player]['car'])*100,2)
                        fig = create_circular_progress_bar(eff_car_pct, 'car_eff', 'blue')
                        st.plotly_chart(fig,use_container_width=True)
    #endregion
    
#region player_yot           
with player_yot_exp:
    cols = st.columns([0.05,0.3,0.3,0.3,0.05])
    df = pd.read_csv('./data/FSU-GT-08-24-24-PLAYS')
    skill_players = df['player'].unique().tolist()
    i = -1
    cols[1].success('consistent! efficient movements of the ball agnostic of game clock.')
    cols[2].warning('low production but dependable target.')
    cols[3].warning('potentially detrimental incompletions. productive in clutch time.')
    for player in skill_players:
        i += 1
        df_player = df[df['player']==player]  
        if len(df_player) < 3:
            i -= 1
            continue
        with cols[(i%3)+1]:
            # Create a new figure for each player
            fig, ax = plt.subplots()
            # Plot yards vs. index for the current player (using index as x-axis)
            ax.plot(df_player.index, df_player['yds'], marker='o', label=player)
            if player == 'king':
                df_rec = df[df['action']=='rec']
                ax.plot(df_rec.index, df_rec['yds'], marker='o', label=player+' passing')
            # Label the axes and title
            ax.set_xlabel('Play')
            ax.set_ylabel('Yards (yds)')
            ax.set_title('yds over time')
            # Add a legend
            ax.legend()
            # Display the plot in Streamlit
            st.pyplot(fig)
    cols[1].success('great balance for our offense.')
    cols[2].success('RB2!')

                
            
#endregion    
    






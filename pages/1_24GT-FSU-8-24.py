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

data = pd.read_csv('./data/FSU-GT-08-24-24-PLAYS')

#region styling

st.markdown("""
<style>

	.stTabs [data-baseweb="tab-list"] {
		gap: 20px;
    }
	.stTabs [data-baseweb="tab"] {
		height: 50px;
        width: 100px;
        white-space: pre-wrap;
		background-color: #F0F2F6;
		border-radius: 4px 4px 0px 0px;
		gap: 1px;
		padding-top: 10px;
		padding-bottom: 10px;
    }
	.stTabs [aria-selected="true"] {
  		background-color: #FFFFFF;
	}
 
    section[data-testid="stSidebar"] {
        width: 310px !important;
    }
    .st-emotion-cache-1i55tjj {
        display: none;
    } 
    .css-1nm2qww {
        display: none;
    }
    .css-vk3wp9 {
        min-width: 309px;
        max-width: 310px;
    }

</style>""", unsafe_allow_html=True)

#endregion

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

    # Calculate the progress and remainder explicitly
    progress_value = percentage
    remainder_value = 100 - percentage

    # Add a single trace to control both progress and remainder
    fig.add_trace(go.Pie(
        values=[progress_value, remainder_value],
        hole=0.7,
        marker=dict(
            colors=[color, '#e6e5e3'],  # Progress color and gray for remainder
            line=dict(color='black', width=1)  # Black outline
        ),
        direction='counterclockwise',  # Force clockwise direction
        rotation=0,  # Start at the bottom
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
        width=80,  # Adjust size for better alignment
        height=80,
        paper_bgcolor="rgba(0,0,0,0)"  # Transparent background
    )
    

    return fig

def create_semi_circular_gauge(percentage, title_input, color_input):
    # Determine the color based on input
    color = '#0afa46' if color_input == 'green' else (
        '#2499ff' if color_input == 'blue' else '#e38c00'
    )

    # Create a semi-circular gauge
    fig = go.Figure()

    if color_input == 'grey':
        color = '#d6d6d6'
        # Add the gauge
        fig.add_trace(go.Indicator(
            mode="gauge",
            value=10,
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': color},  # Progress bar color
                'bgcolor': "white",  # Background color
                'steps': [
                    {'range': [0, 100], 'color': '#f2eded'}  # Background color for gauge
                ],
                'threshold': {
                    'line': {'color': color, 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            },
        ))
    else:
        # Add the gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=percentage,
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': color},  # Progress bar color
                'bgcolor': "white",  # Background color
                'steps': [
                    {'range': [0, 100], 'color': '#e6e5e3'}  # Background color for gauge
                ],
                'threshold': {
                    'line': {'color': color, 'width': 4},
                    'thickness': 0.75,
                    'value': percentage
                }
            },
        ))

    # Update layout for a semi-circle effect
    fig.update_layout(
        margin=dict(t=5, b=5, l=5, r=5),
        width=100,
        height=75,
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
    )

    return fig

#endregion

header = st.container()
header_cols = header.columns(5)
notes = load_notes(notes_file_path)
    
with header_cols[0].popover('ℹ️Info', use_container_width=True):
    for note in notes:
        st.warning('* '+note)
        
editor_exp = st.expander('editor')
dashboard_exp = st.expander('dashboard')
off_playbook_exp = st.expander('offensive review')
player_eval_exp = st.expander('offensive player eval')

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

#region dashboard

with dashboard_exp:

    add_vertical_space(2)
    team_metrics, team_graphs = st.tabs(['team_metrics','team_graphs'])   
    
    metrics = {
        'plays':0,'total_yds':0,'avg_yds':0,'offensive_efficacy':0,
        'pass_ratio':0,'pass_yds':0,'rec_avg':0,'pass_efficiency':0,
        'rush_ratio':0,'rush_yds':0,'car_avg':0,'rush_efficiency':0,
        'completion_pct':0,'yd_contribution':0,'total_conversion_rate':0,'third_conversion_rate':0
    }
    
    df = data.copy()
    # Passing Plays / Rushing Plays
    plays = len(df)
    metrics['plays'] = plays
    passing_df = df[df['action']=='rec']
    rushing_df = df[df['action']=='rush']
    # Pass / Rush Ratio
    p_ratio = len(passing_df)/plays
    r_ratio = 1 - p_ratio
    metrics['pass_ratio'] = p_ratio
    metrics['rush_ratio'] = r_ratio
    # Avg Yds per Rec
    completed_df = passing_df[passing_df['completed']==True]
    rec_avg = completed_df['yds'].mean()
    metrics['rec_avg'] = rec_avg
    # Avg Yds per Carry
    car_avg = rushing_df['yds'].mean()
    metrics['car_avg'] = car_avg
    # Avg Yds per play
    avg_yds = df['yds'].mean()
    metrics['avg_yds'] = avg_yds
    # Pass Yds
    pass_yds = passing_df['yds'].sum()
    metrics['pass_yds'] = pass_yds
    # Rush Yds
    rush_yds = rushing_df['yds'].sum()
    metrics['rush_yds'] = rush_yds
    # Total Yds
    total_yds = pass_yds + rush_yds
    metrics['total_yds'] = total_yds
    # Completion %
    comp_pct = len(completed_df)/len(passing_df)
    metrics['completion_pct'] = comp_pct
    # Effective Receptions
    eff_rec_df = passing_df[(passing_df['yds']>5.0) | (passing_df['converted']==True)]
    # Effective Carries
    eff_car_df = rushing_df[(rushing_df['yds']>5.0) | (rushing_df['converted']==True)]
    # Effective Plays
    eff_plays_df = df[(df['yds']>5.0) | (df['converted']==True)]
    # Passing Efficacy 
    pass_efficacy = len(eff_rec_df)/len(passing_df)
    metrics['pass_efficiency'] = pass_efficacy
    # Rushing Efficacy
    rush_efficacy = len(eff_car_df)/len(rushing_df)
    metrics['rush_efficiency'] = rush_efficacy
    # Efficient Movement %
    offensive_efficacy = len(eff_plays_df)/plays
    metrics['offensive_efficacy'] = offensive_efficacy
    # Conversion Rate
    conversion_df = df[df['converted']==True]
    conversion_rate = len(conversion_df)/plays
    metrics['total_conversion_rate'] = conversion_rate
    # Third_conversion_rate
    third_df = df[df['down']==3]
    third_conversion_df = third_df[third_df['converted']==True]
    third_conversion_rate = len(third_conversion_df)/len(third_df)
    metrics['third_conversion_rate'] = third_conversion_rate
    
    # Team Graph
    df_team_graph = data.copy()
    df_team_graph['efficient'] = (df_team_graph['yds']>5.0) | (df_team_graph['converted']==True)
    df_team_graph['efficiency'] = df_team_graph['efficient'].expanding().mean()
    df_team_graph['yds_positive'] = df_team_graph['yds'].apply(lambda x: x if x > 0 else 0)
    df_team_graph['yds_total_positive'] = df_team_graph['yds_positive'].cumsum()
    df_team_graph['contributing_yds'] = df_team_graph.apply(lambda x: x['yds'] * x['contributed'], axis=1)
    df_team_graph['contributing_yds_total'] = df_team_graph['contributing_yds'].cumsum()
    df_team_graph['contributing_yds%'] = df_team_graph['contributing_yds_total'] / df_team_graph['yds_total_positive']
    
    # Contributing Yds
    contributing_yds = df_team_graph['contributing_yds'].sum()
    total_positive_yds = df_team_graph['yds_positive'].sum()
    # Yd Contribution %
    yd_contribution = contributing_yds/total_positive_yds
    metrics['yd_contribution'] = yd_contribution
    
    
    with team_metrics:
        cont_cols = st.columns([0.13,0.13,0.13,0.13,0.48])
        for i,metric in enumerate(metrics.keys()):
            with cont_cols[i%4]:
                with stylable_container(
                    key=f"container_with_border_{metric}",
                    css_styles="""
                        {
                            border: 2px solid rgba(100, 100, 100, 0.5);
                            border-radius: 0.5rem;
                            padding: calc(1em - 1px)
                            
                        }
                        """,
                    ):
                    st.metric(label=metric,value=round(metrics[metric],2))

        legend = [
            'an efficient movement advances the ball >= 5 yds or converts',
            'offensive efficacy = number of efficient movements / total plays',
            'pass efficiency = efficient passes / attempts',
            'rush efficiency = efficient rushes / attempts',
            'yd contribution = positive yds leading to a score / total positive yds' 
        ]

        with cont_cols[4]:
            with stylable_container(
                    key="container_with_border_black",
                    css_styles="""
                        {
                            border: 1px solid rgba(100, 100, 100, 0.5);
                            border-radius: 0.5rem;
                            padding: 10px;
                        }
                        """,
                ):
                    st.markdown(f"<h3 style='text-align: center; color: black; font-size: 14px;'>Notes</p>", unsafe_allow_html=True)
                    for i in legend:
                        st.info(i)
                    add_vertical_space(2)   
        
    with team_graphs:
        cont_cols = st.columns([0.05,0.3,0.3,0.3,0.05])
        
        with cont_cols[1]:
            fig, ax = plt.subplots()
            # Plot yards vs. index for the current player (using index as x-axis)
            ax.plot(df_team_graph.index, df_team_graph['efficiency'], marker='o', label='efficient movement %', color='#00d443')
            ax.plot(df_team_graph.index, df_team_graph['contributing_yds%'], marker='o', label='yd contribution %', color='#f736ee')
            
            line = [0.5]*df.shape[0]
            ax.plot(df.index, line)
            ax.annotate(
                '0.5',  # Text to display
                xy=(0, 0.5),         # Point to annotate
                xytext=(-0.5, 0.51),  # Text position
                fontsize=12,                       # Font size
                color='black'                       # Text color
            )
            
            # Annotate the last point of the main plot (avg column)
            last_index = df_team_graph.index[-1]
            last_avg = df_team_graph['contributing_yds%'].iloc[-1]
            ax.annotate(
                f'({last_avg:.2f})',  # Text to display
                xy=(last_index, last_avg),         # Point to annotate
                xytext=(last_index-3, last_avg+0.03),  # Text position
                fontsize=12,                       # Font size
                color='black'                       # Text color
            )
            
            # Annotate the last point of the main plot (avg column)
            last_index = df_team_graph.index[-1]
            last_avg = df_team_graph['efficiency'].iloc[-1]
            ax.annotate(
                f'({last_avg:.2f})',  # Text to display
                xy=(last_index, last_avg),         # Point to annotate
                xytext=(last_index-3, last_avg+0.02),  # Text position
                fontsize=12,                       # Font size
                color='black'                       # Text color
            )
            
            
            # limit the y axis manually
            plt.ylim(last_avg-0.16,1.03)
            
            
            # Label the axes and title
            ax.set_xlabel('Play')
            ax.set_title('Efficiency / time')
            # Add a legend
            ax.legend()
            # Display the plot in Streamlit
            st.pyplot(fig)

            

#endregion

#region off_playbook

with off_playbook_exp:
    
    add_vertical_space(2)
    gt_terr, opp_terr, red_zone, all_plays = st.tabs(['gt_terr','opp_terr','red_zone','all_plays'])   
    df = data.copy()
    df = df[['down', 'ytg', 'field_pos', 'player', 'action', 'completed', 'yds', 'converted']]
    with gt_terr:
        gt_terr_first_container = st.container()
        gt_terr_third_container = st.container()
        cols_first = gt_terr_first_container.columns([0.01,0.49,0.49,0.01])
        cols_third = gt_terr_third_container.columns([0.01,0.49,0.49,0.01])
        with cols_first[1]:
            df_gt_terr = df[df['field_pos']<50]
            df_gt_terr_first = df_gt_terr[df_gt_terr['down']==1]
            df_gt_terr_first = df_gt_terr_first.sort_values(['action','yds'],ascending=True)
            st.table(df_gt_terr_first)
        with cols_first[2]:
            add_vertical_space(2)
            st.success('4/5 passes completed (80%) on 1st down in GT territory')
            st.success('5/8 effective carries (62.5%) on 1st down in GT territory')
            st.success('8/13 efficient movements (61.5%) of the ball on 1st down in GT territory.')
            st.success('5/13 conversions (38.5%) on 1st down in GT territory. Approaching 40% with our Pass/Rush Ratio and efficacy is elite.')
        with cols_third[1]:
            df_gt_terr_third = df_gt_terr[df_gt_terr['down']==3]
            df_gt_terr_third = df_gt_terr_third.sort_values(['action','yds'],ascending=True)
            st.table(df_gt_terr_third)
        with cols_third[2]:
            add_vertical_space(1)
            st.success('2/4 conversions (50%) on 3rd down in GT territory')
            
            
    with opp_terr:   
        opp_terr_first_container = st.container()
        opp_terr_third_container = st.container()
        cols_first = opp_terr_first_container.columns([0.01,0.49,0.49,0.01])
        cols_third = opp_terr_third_container.columns([0.01,0.49,0.49,0.01])
        with cols_first[1]:
            df_opp_terr = df[(df['field_pos']>=50)&(df['field_pos']<80)]
            df_opp_terr_first = df_opp_terr[df_opp_terr['down']==1]
            df_opp_terr_first = df_opp_terr_first.sort_values(['action','yds'],ascending=True)
            st.table(df_opp_terr_first)
        with cols_first[2]:    
            add_vertical_space(2)
            st.warning('3/7 efficient movements (42.9%) of the ball on 1st down in between midfield and the red zone. ')
            st.error('0/7 conversions (0%) on 1st down in between midfield and the red zone.')
        with cols_third[1]:  
            df_opp_terr_third = df_opp_terr[df_opp_terr['down']==3]
            df_opp_terr_third = df_opp_terr_third.sort_values(['action','yds'],ascending=True)
            st.table(df_opp_terr_third)
        with cols_third[2]:
            add_vertical_space(1)
            st.success('3/4 efficient movements (75%) of the ball on 3rd down in between midfield and the redzone.')
            st.success('2/4 conversions (50%) on 3rd down in between midfield and the redzone.')
        
    with red_zone:
        red_zone_first_container = st.container()
        red_zone_third_container = st.container()
        cols_first = red_zone_first_container.columns([0.01,0.49,0.49,0.01])
        cols_third = red_zone_third_container.columns([0.01,0.49,0.49,0.01])

        with cols_first[1]:
            df_red_zone = df[df['field_pos']>=80]
            df_red_zone_first = df_red_zone[df_red_zone['down']==1]
            df_red_zone_first = df_red_zone_first.sort_values(['action','yds'],ascending=True)
            st.table(df_red_zone_first)
        with cols_first[2]:
            add_vertical_space(2)
            st.success('3/6 efficient movements (50%) of the ball on 1st down in the redzone.')
            st.warning('0 passes in 6 redzone 1st downs.') 
        with cols_third[1]:    
            df_red_zone_third = df_red_zone[df_red_zone['down']==3]
            df_red_zone_third = df_red_zone_third.sort_values(['action','yds'],ascending=True)
            st.table(df_red_zone_third)
        with cols_third[2]:
            add_vertical_space(1)
            st.success('3rd and goal.... hand it off to Jamal.')
        
    with all_plays:
        cols = st.columns([0.01,0.98,0.01])
        with cols[1]:
            st.dataframe(data, use_container_width=True, height=600)
        
        
#endregion

#region player_eval
           
with player_eval_exp:
    add_vertical_space(2)
    player_cards, yot, avg_yot = st.tabs(["player cards","yds/t","avg yds/t"])    
    
    with player_cards:
        player_cards_container = st.container()
        with player_cards_container:
            cols = st.columns([0.3,0.3,0.3])
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
                with cols[i%3]:  
                    with stylable_container(
                        key=f"container_with_border_{player}",
                        css_styles="""
                            {
                                border: 2px solid rgba(100, 100, 100, 0.5);
                                border-radius: 0.5rem;
                                padding: calc(1em - 1px)
                                
                            }
                            """,
                        ):
                        container_cols = st.columns([0.05,0.45,0.45,0.05])
                        with container_cols[1]:
                            add_vertical_space(1)
                            st.markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>{player}</p>", unsafe_allow_html=True)
                            image = "./pics/"+player+".jpg"
                            base64_image = get_image_as_base64(image)
                            markdown_str = f"""<div style="text-align:center;"><img src="data:image/jpeg;base64,{base64_image}" alt="{player}" width="200" style="border-radius:10px;"></div>"""
                            st.markdown(markdown_str, unsafe_allow_html=True)
                            add_vertical_space(3)
                            
                        with container_cols[2]:
                            add_vertical_space(2)
                            st.write(sorted_data[player])
                        
                        
                        if player != 'king':
                            if sorted_data[player]['targets'] > 0:
                                cmp_pct = round((sorted_data[player]['rec']/sorted_data[player]['targets'])*100,2)
                                container_cols[1].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>cmp%</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(cmp_pct, 'rec_eff','green')
                                container_cols[1].plotly_chart(fig,use_container_width=True,key=player+'cmp',theme=None)
                                add_vertical_space(1)
                            else:
                                container_cols[1].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>N/A</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(0, 'rec_eff','grey')
                                container_cols[1].plotly_chart(fig,use_container_width=True,key=player+'cmp',theme=None)
                                add_vertical_space(1)
                            if sorted_data[player]['car'] > 0:
                                eff_car_pct = round((sorted_data[player]['eff_car']/sorted_data[player]['car'])*100,2)
                                container_cols[2].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>eff_car%</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(eff_car_pct, 'car_eff', 'blue')
                                container_cols[2].plotly_chart(fig,use_container_width=True,key=player+'eff',theme=None)
                                add_vertical_space(1)
                            else:
                                container_cols[2].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>N/A</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(0, 'car_eff','grey')
                                container_cols[2].plotly_chart(fig,use_container_width=True,key=player+'eff',theme=None)
                                add_vertical_space(1)
                        else:
                            if sorted_data[player]['att'] > 0:
                                cmp_pct = round((sorted_data[player]['cmp']/sorted_data[player]['att'])*100,2)
                                container_cols[1].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>cmp%</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(cmp_pct, 'cmp','orange')
                                container_cols[1].plotly_chart(fig,use_container_width=True,key=player+'cmp',theme=None)
                                add_vertical_space(1)
                            if sorted_data[player]['car'] > 0:
                                eff_car_pct = round((sorted_data[player]['eff_car']/sorted_data[player]['car'])*100,2)
                                container_cols[2].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>eff_car%</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(eff_car_pct, 'car_eff', 'blue')
                                container_cols[2].plotly_chart(fig,use_container_width=True,key=player+'eff',theme=None)
                                add_vertical_space(1)
                            else:
                                container_cols[2].markdown(f"<p style='text-align: center; color: black; font-size: 14px;'>N/A</p>", unsafe_allow_html=True)
                                fig = create_semi_circular_gauge(0, 'car_eff','grey')
                                container_cols[2].plotly_chart(fig,use_container_width=True,key=player+'eff',theme=None)
                                add_vertical_space(1)
                        
    with yot:
        cols = st.columns([0.05,0.3,0.3,0.3,0.05])
        df = pd.read_csv('./data/FSU-GT-08-24-24-PLAYS')
        skill_players = df['player'].unique().tolist()
        i = -1
        
        player_notes = {
            'haynes': ['green', 'consistent! efficient movements of the ball agnostic of game clock.'],
            'singleton': ['yellow', 'low production but dependable target. \n  '],
            'rutherford': ['yellow', 'potentially detrimental incompletions. productive in clutch time.'],
            'king': ['yellow', 'decent balance for our offense. Rushing needs to improve.'],
            'alexander': ['green', 'RB2!']
        }
        
        
        with cols[3]:
            add_vertical_space(1)
            with stylable_container(
                    key="container_with_border_black",
                    css_styles="""
                        {
                            border: 1px solid rgba(100, 100, 100, 0.5);
                            border-radius: 0.5rem;
                            padding: 10px;
                        }
                        """,
                ):
                    add_vertical_space(1)   
                    st.markdown(f"<h3 style='text-align: center; color: black; font-size: 14px;'>Notes</p>", unsafe_allow_html=True)
                    for player in skill_players:
                        if player in player_notes.keys():
                            if player_notes[player][0] == 'green':
                                st.success(player+': '+player_notes[player][1])
                            elif player_notes[player][0] == 'yellow':
                                st.warning(player+': '+player_notes[player][1])
                            else:
                                st.error(player+': '+player_notes[player][1]) 
                    add_vertical_space(2)            
                    
             
             
        for player in skill_players:            
            i += 1
            df_player = df[df['player']==player]  
            if len(df_player) < 3:
                i -= 1
                continue

            with cols[(i%2)+1]:
                
                # Create a new figure for each player
                fig, ax = plt.subplots()
                # Plot yards vs. index for the current player (using index as x-axis)
                ax.plot(df_player.index, df_player['yds'], marker='o', label=player)
                line = [5]*df.shape[0]
                ax.plot(df.index, line)
                if player == 'king':
                    df_rec = df[df['action']=='rec']
                    ax.plot(df_rec.index, df_rec['yds'], marker='o', label=player+' passing')
                ax.annotate(
                    '5',  # Text to display
                    xy=(0, 5),         # Point to annotate
                    xytext=(-0.5, 5),  # Text position
                    fontsize=12,                       # Font size
                    color='black'                       # Text color
                )    
                # Label the axes and title
                ax.set_xlabel('Play')
                ax.set_ylabel('Yards (yds)')
                ax.set_title('yds / time')
                # Add a legend
                ax.legend()
                # Display the plot in Streamlit
                st.pyplot(fig)
    
    with avg_yot:
        top = st.container()
        mid = st.container()
        bot = st.container()
        top_cols = top.columns([0.05,0.3,0.3,0.3,0.05])
        mid_cols = mid.columns([0.05,0.3,0.3,0.3,0.05])
        bot_cols = bot.columns([0.05,0.3,0.3,0.3,0.05])
        df = pd.read_csv('./data/FSU-GT-08-24-24-PLAYS')
        skill_players = df['player'].unique().tolist()
        i = -1
        
        # Top Row Notes
        
        for player in skill_players:
            i += 1
            df_player = df[df['player']==player]  
            df_player['avg'] = df_player['yds'].expanding().mean()
            if len(df_player) < 3:
                i -= 1
                continue
            with mid_cols[(i%3)+1]:
                # Create a new figure for each player
                fig, ax = plt.subplots()
                # Plot yards vs. index for the current player (using index as x-axis)
                ax.plot(df_player.index, df_player['avg'], marker='o', label=player)
                line = [5]*df.shape[0]
                ax.plot(df.index, line)
                ax.annotate(
                    '5',  # Text to display
                    xy=(0, 5),         # Point to annotate
                    xytext=(-0.5, 5),  # Text position
                    fontsize=12,                       # Font size
                    color='black'                       # Text color
                )
                if player == 'king':
                    df_rec = df[df['action']=='rec']
                    df_rec['avg'] = df_rec['yds'].expanding().mean()
                    ax.plot(df_rec.index, df_rec['avg'], marker='o', label=player+' passing')
                    last_index = df_rec.index[-1]
                    last_avg = df_rec['avg'].iloc[-1]
                    ax.annotate(
                        f'({last_avg:.2f})',  # Text to display
                        xy=(last_index, last_avg),         # Point to annotate
                        xytext=(last_index-1.5, last_avg+1.5),  # Text position
                        fontsize=12,                       # Font size
                        color='black'                       # Text color
                    )
                
                # Annotate the last point of the main plot (avg column)
                last_index = df_player.index[-1]
                last_avg = df_player['avg'].iloc[-1]
                ax.annotate(
                    f'({last_avg:.2f})',  # Text to display
                    xy=(last_index, last_avg),         # Point to annotate
                    xytext=(last_index-1.5, last_avg+1.5),  # Text position
                    fontsize=12,                       # Font size
                    color='black'                       # Text color
                )
                
                # Label the axes and title
                ax.set_xlabel('Play')
                ax.set_ylabel('Yards (yds)')
                ax.set_title('avg yds / time')
                # Add a legend
                ax.legend()
                # Display the plot in Streamlit
                st.pyplot(fig)
                

   
                
#endregion  




          
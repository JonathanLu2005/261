import psycopg2
import matplotlib
matplotlib.use('Agg')  # Ensures plots are saved without a GUI
import matplotlib.pyplot as plt
import os
import numpy as np

def get_database_connection():
    """Establish a connection to the database."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "dpg-cuo9l73qf0us738ub4gg-a.frankfurt-postgres.render.com"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "db_261database"),
            user=os.getenv("DB_USER", "db_261database_user"),
            password=os.getenv("DB_PASS", "vLblDDUVURf4vKa8MExB8d1hiwWAIQg8")
        )
        return connection
    except Exception as e:
        print(f"Error during database connection: {e}")
        return None

def get_last_junction_id_and_name(modelid, conn):
    """Get the last junction ID and name for a given model ID."""
    
    # Uses the logic that database serial values will go in ascending order and as such the junction parameters the user has just inputted will have the highest id number
    query = """
        SELECT junctionid, junctionname 
        FROM junctionconfigurations 
        WHERE modelid = %s 
        ORDER BY junctionid DESC LIMIT 1
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (modelid,))
        # gets the first entry
        result = cursor.fetchone()
    return result if result else (None, None)


def plot_current_junction(junction_id, junction_name, conn, metric, ylabel, title):
    # Generic function to plot different performance metrics.
    query = f"""
        SELECT north{metric}, south{metric}, east{metric}, west{metric} 
        FROM junctionperformance 
        WHERE junctionid = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (junction_id,))
        data = cursor.fetchone()


    if data:
        directions = ["North", "South", "East", "West"]
        plt.figure(figsize=(8, 5))
        plt.bar(directions, data, color='blue')
        plt.xlabel('Direction')
        plt.ylabel(ylabel)
        plt.title(f"{title} for {junction_name}")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save as a png file
        filename = f"static/images/{junction_name}_{metric}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Graph saved as {filename}")
        return filename
    else:
        print(f"No data found for junction: {junction_id}")
        return None

def plot_all_junctions(model_id, conn, metric, ylabel, title):
    # Generic function to plot performance metrics for all junctions in a model.
    query = f"""
        SELECT j.junctionname, p.north{metric}, p.south{metric}, p.east{metric}, p.west{metric}
        FROM junctionperformance p
        JOIN junctionconfigurations j ON p.junctionid = j.junctionid
        WHERE j.modelid = %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (model_id,))
        results = cursor.fetchall()

    if results:
        directions = ['North', 'South', 'East', 'West']
        junctions = [row[0] for row in results]
        num_junctions = len(junctions)

        # Gets the data as a dictionary for each direction from th results array
        performance_data = {dir: [row[i+1] for row in results] for i, dir in enumerate(directions)}

        x = np.arange(len(directions))
        width = 0.15

        fig, ax = plt.subplots(figsize=(12, 6))

        # Ensures the directions on the x-axis are centered for the bar graph
        shift = np.linspace(-((num_junctions - 1) / 2) * width, 
                            ((num_junctions - 1) / 2) * width, 
                            num_junctions)

        for i, junction in enumerate(junctions):
            ax.bar(x + shift[i], 
                   [performance_data[dir][i] for dir in directions], 
                   width, 
                   label=f'Junction {junction}')

        ax.set_xticks(x)
        ax.set_xticklabels(directions, rotation=0)
        ax.set_xlabel('Directions')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(title="Junctions")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save as a png file
        filename = f"Model_{model_id}_{metric}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Graph saved as {filename}")

    else:
        print(f"No data found for model ID: {model_id}")

# Here are the functions to call. Takes the model id as a parameter and produces a bar graph.
def plot_max_wait_time_current_junction(modelid):
    with get_database_connection() as conn:
        junction_id, junction_name = get_last_junction_id_and_name(modelid, conn)
        if junction_id:
            plot_current_junction(junction_id, junction_name, conn, "maximumwaittime", "Maximum Wait Time (seconds)", "Maximum Wait Time per Direction")

def plot_avg_wait_time_current_junction(modelid):
    with get_database_connection() as conn:
        junction_id, junction_name = get_last_junction_id_and_name(modelid, conn)
        if junction_id:
            plot_current_junction(junction_id, junction_name, conn, "averagewaittime", "Average Wait Time (seconds)", "Average Wait Time per Direction")

def plot_max_queue_length_current_junction(modelid):
    with get_database_connection() as conn:
        junction_id, junction_name = get_last_junction_id_and_name(modelid, conn)
        if junction_id:
            plot_current_junction(junction_id, junction_name, conn, "maximumqueuelength", "Maximum Queue Length", "Maximum Queue Length per Direction")

def plot_max_wait_time_all_junctions(model_id):
    with get_database_connection() as conn:
        plot_all_junctions(model_id, conn, "maximumwaittime", "Maximum Wait Time (seconds)", "Maximum Wait Time per Direction for All Junctions")

def plot_avg_wait_time_all_junctions(model_id):
    with get_database_connection() as conn:
        plot_all_junctions(model_id, conn, "averagewaittime", "Average Wait Time (seconds)", "Average Wait Time per Direction for All Junctions")

def plot_max_queue_length_all_junctions(model_id):
    with get_database_connection() as conn:
        plot_all_junctions(model_id, conn, "maximumqueuelength", "Maximum Queue Length", "Maximum Queue Length per Direction for All Junctions")


# Calculates the junction ranking and adds it to the database. TO DO: Improve min,max for each variable
def calculate_junction_ranking(junctionid, avgwaittimeweight, maxwaittimeweight, maxqueuelengthweight):
    minAvgWaitTime = 0
    maxAvgWaitTime = 400
    minMaxWaitTime = 0
    maxMaxWaitTime = 600
    minMaxQueueLength = 0
    maxMaxQueueLength = 50
    # SQL Queries
    meanAvgWaitTimeQuery = '''
        SELECT (northaveragewaittime + southaveragewaittime + eastaveragewaittime + westaveragewaittime) / 4.0 
        AS mean_average_wait_time FROM junctionperformance WHERE junctionid = %s;'''

    meanMaxWaitTimeQuery = '''
        SELECT (northmaximumwaittime + southmaximumwaittime + eastmaximumwaittime + westmaximumwaittime) / 4.0 
        AS mean_maximum_wait_time FROM junctionperformance WHERE junctionid = %s;'''

    meanMaxQueueLengthQuery = '''
        SELECT (northmaximumqueuelength + southmaximumqueuelength + eastmaximumqueuelength + westmaximumqueuelength) / 4.0 
        AS mean_maximum_queue_length FROM junctionperformance WHERE junctionid = %s;'''

    # Connect to Database
    
    conn, cursor = get_database_connection()
    if not conn or not cursor:
        print("Failed to connect to the database.")
        return

    # Retrieves data from the database
    cursor.execute(meanAvgWaitTimeQuery, (junctionid,))
    data = cursor.fetchone()
    meanAvgWaitTime = data[0] if meanAvgWaitTime else 0

    cursor.execute(meanMaxWaitTimeQuery, (junctionid,))
    data = cursor.fetchone()
    meanMaxWaitTime = data[0] if meanMaxWaitTime else 0

    cursor.execute(meanMaxQueueLengthQuery, (junctionid,))
    data = cursor.fetchone()
    meanMaxQueueLength = data[0] if meanMaxQueueLength else 0

        # Inverted Normalization (Better = Higher Score)
    normAvgWaitTime = 1 - ((meanAvgWaitTime - minAvgWaitTime) / (maxAvgWaitTime - minAvgWaitTime))
    normMaxWaitTime = 1 - ((meanMaxWaitTime - minMaxWaitTime) / (maxMaxWaitTime - minMaxWaitTime))
    normMaxQueueLength = 1 - ((meanMaxQueueLength - minMaxQueueLength) / (maxMaxQueueLength - minMaxQueueLength))

        # Weighted ranking
    junctionRanking = (normAvgWaitTime * avgwaittimeweight) +(normMaxWaitTime * maxwaittimeweight) + (normMaxQueueLength * maxqueuelengthweight)
    
    updateRankingQuery = '''
        UPDATE junctionperformance
        SET junction_ranking = %s
        WHERE junctionid = %s;
    '''
    # Store ranking into the database
    cursor.execute(updateRankingQuery, (junctionRanking, junctionid))
    conn.commit()  # Save changes
  

def plot_junction_rankings_for_model(modelid):
    # SQL Query to retrieve junction rankings for a given model
    query = '''
        SELECT jc.junctionname, jp.overalljunctionscore
        FROM junctionconfigurations jc
        JOIN junctionperformance jp ON jc.junctionid = jp.junctionid
        WHERE jc.modelid = %s;
    '''

    conn, cursor = get_database_connection()
    if not conn or not cursor:
        print("Failed to connect to the database.")
        return    

        # Fetch junction rankings for the given model ID
    cursor.execute(query, (modelid,))
    results = cursor.fetchall()

    if not results:
        print(f"No junction rankings found for model ID {modelid}")
        return
        
        # Extract junction names and rankings
    junction_names = [row[0] for row in results]
    rankings = [row[1] for row in results]

        # Plot the rankings
    plt.figure(figsize=(10, 5))
    plt.bar(junction_names, rankings, color='skyblue')
    plt.xlabel('Junctions')
    plt.ylabel('Ranking Score')
    plt.title(f'Junction Rankings for Model ID {modelid}')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
        
    # Save the plot
    plt.savefig("Junction_Rating_Graph.jpg", bbox_inches='tight', dpi=300)
    plt.close()





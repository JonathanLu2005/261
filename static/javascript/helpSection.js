/* For help section */
const texts = {
    /* Texts for different parts of help section */
    overview: `
        Challenged by restricted resources, councils have had limited success in improving road networks. This warrants the
        creation of a system to allow users to model junctions and simulate their traffic flow to determine their effectiveness.
        Allowing multiple solutions to be evaluated, users are able to find optimal junction configurations cost-effectively.
        For the user to identify the most effective junction configuration, they control several parameters like the number of
        lanes, vehicles per hour, and more to design their junction. Based on these parameters, the system will simulate the
        junction’s handling of traffic to determine the maximum and average waiting times of the vehicles alongside the maximum
        queue length from each direction of the junction. The model will combine these stated metrics into an overall rating of
        the junction’s effectiveness, allowing the user to effortlessly compare different junction parameters and identify optimal
        solutions. The interface will be a website where the user can simulate different junction configurations. Users can create model
        spaces (folders) to separate their junctions by location and how traffic flow may vary, as the user may create junctions
        for different areas.
    `,
    interface: `
        On the home page, users can create their models, then enter their models to add junctions. This intuitive interface allows
        users to structure their workspaces effectively and focus on creating optimised junction configurations.
    `,
    modelData: `
        <ul>
            <li><strong>Simulation Length:</strong> Length of the simulation in seconds.</li>
            <li><strong>Vehicle Speed:</strong> Speed of cars in mph.</li>
            <li><strong>Vehicle Length:</strong> Length of cars in meters.</li>
            <li><strong>Vehicle Fluctuation Length:</strong> Fluctuation range for car length.</li>
            <li><strong>Vehicle Stationary Distance:</strong> Distance between stationary cars in meters.</li>
            <li><strong>Vehicle Reaction Time:</strong> Reaction time of cars.</li>
            <li><strong>Vehicle Per Hour:</strong> Array of traffic flow values for each direction.</li>
            <li><strong>Bus/Cycle Length:</strong> Length of bus/cycle.</li>
            <li><strong>Bus/Cycle Speed:</strong> Speed of bus/cycle.</li>
            <li><strong>Bus/Cycle Fluctuation Length:</strong> Fluctuation range for bus/cycle.</li>
            <li><strong>Bus/Cycle Per Hour:</strong> Traffic flow values for bus/cycle.</li>
        </ul>
    `,
    junctionData: `
        <ul>
            <li><strong>Junction Side Length:</strong> The side length of the junction in meters.</li>
            <li><strong>General Lanes:</strong> Number of general lanes (excluding bus and cycle lanes).</li>
            <li><strong>Left Turn Lane:</strong> Indicates if the junction has left-turn lanes.</li>
            <li><strong>Right Turn Lane:</strong> Indicates if the junction has right-turn lanes.</li>
            <li><strong>Pedestrian Crossing:</strong> Indicates if there are pedestrian crossings.</li>
            <li><strong>Pedestrian Time:</strong> Duration of pedestrian crossings in seconds.</li>
            <li><strong>Pedestrian Crossing Requests Per Hour:</strong> Frequency of pedestrian crossings per hour.</li>
            <li><strong>Traffic Light Sequence:</strong> The sequence of traffic lights.</li>
            <li><strong>Traffic Light Green Times:</strong> Green light duration for each direction.</li>
            <li><strong>Bus/Cycle Lane:</strong> Indicates if there is a bus or cycle lane.</li>
            <li><strong>Bus/Cycle Ratio:</strong> Ratio of green light time allocated to bus/cycle.</li>
        </ul>
    `
};

/* Changes text of help section when clicked on */
function changeText(section) {
    document.getElementById('main-text').innerHTML = texts[section];
}

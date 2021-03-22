using namespace std;

#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <set>
#include <string>

typedef pair<int, int> Node;

/**
 * Read labrunth data from the specified file
 */
vector<string> read_labrynth(string file_path) {
    string line;
    vector<string> labrynth;
    ifstream labrynth_file(file_path);

    while (getline(labrynth_file, line)) {
        labrynth.push_back(line);
    }
    labrynth_file.close();
    return labrynth;
}


/**
 * Helper function to check whether a particular cell is considered as space
 */
bool is_space_available(char c) {
    return c == '.';
}

/**
 * Find positions in horizontal and vertical directions which are also filled with '.'
 */
vector<Node> get_neighbours(vector<string> labrynth, int row, int col) {
    vector<Node> neighbours;
    int row_max = labrynth.size();
    int col_max = labrynth[row].size();

    // Neighbours are in 4 directions - up, down, right, left
    // Depending on the position, a cell might have limited set of neighbours
    if (row + 1 < row_max && is_space_available(labrynth[row + 1][col])) {
        neighbours.push_back(Node(row + 1, col));
    }

    if (row - 1 >= 0 && is_space_available(labrynth[row - 1][col])) {
        neighbours.push_back(Node(row - 1, col));
    }

    if (col + 1 < col_max && is_space_available(labrynth[row][col + 1])) {
        neighbours.push_back(Node(row, col + 1));
    }

    if (col - 1 >= 0 && is_space_available(labrynth[row][col - 1])) {
        neighbours.push_back(Node(row, col - 1));
    }
    return neighbours;
}

/**
 * Get a mapping of all empty cells to its empty nighbours
 */
map<Node, vector<Node>> get_adjacency_list(vector<string> labrynth) {
    map<Node, vector<Node>> adjancency_list;
    for (int row = 0; row < labrynth.size(); row++) {
        for (int col = 0; col < labrynth[row].size(); col++) {
            if (is_space_available(labrynth[row][col])) {
                Node node(row, col);
                adjancency_list.insert(make_pair(node, get_neighbours(labrynth, row, col)));
            }
        }
    }
    return adjancency_list;
}

/**
 * Find all postions in first row that have '.'
 */
vector<Node> get_entrances(string first_row) {
    vector<Node> entrances;
    for (int index = 0; index < first_row.size(); index++) {
        if (is_space_available(first_row[index])) {
            entrances.push_back(make_pair(0, index));
        }
    }
    return entrances;
}

/**
 * Recursively navigate all paths to find the longest path from a particular entrance
 */
void navigate(Node node, map<Node, vector<Node>> adjacency_list,
    set<Node>& visited, vector<Node>& longest_path, vector<Node> path) {
    // If node has not been visited already
    if (visited.find(node) == visited.end()) {
        path.push_back(node);
        visited.insert(node);
        if (path.size() > longest_path.size()) {
            longest_path = path;
        }
        // If the node has any neighbours branch to each path
        if (adjacency_list.find(node) != adjacency_list.end()) {
            for (auto neighbour : adjacency_list[node]) {
                // copying the visited set, so that navigating different branches don't interfere with each other
                set<Node> visited_copy(visited);
                navigate(neighbour, adjacency_list, visited_copy, longest_path, path);
            }
        }
    }
}

/**
 * Find longest path from each empty cell in first row
 */
vector<vector<Node>> find_longest_paths(map<Node, vector<Node>> adjacency_list, vector<Node> entrances) {
    vector<vector<Node>> paths;
    for (auto entrance : entrances) {
        set<Node> visited;
        vector<Node> path;
        vector<Node> longest_path;
        navigate(entrance, adjacency_list, visited, longest_path, path);
        paths.push_back(vector<Node>(longest_path));
    }
    return paths;
}

/**
 * Write output to the specified file.
 */
void write_output(vector<string> labrynth, vector<Node> path, string file_path) {
    // Convert char to string representation so that multi-digit numbers can be inserted.
    vector<vector<string>> string_repr;
    for (auto row : labrynth) {
        vector<string> row_str;
        for (auto c : row) {
            row_str.push_back(string(1, c));
        }
        string_repr.push_back(row_str);
    }

    // Replace the '.' with index of node in the path
    for (int index = 0; index < path.size(); index++) {
        string_repr[path[index].first][path[index].second] = to_string(index);
    }

    ofstream output_file(file_path);
    output_file << path.size() << endl;
    for (auto line : string_repr) {
        for (auto word : line) {
            output_file << word;
        }
        output_file << endl;
    }
    output_file.close();
}

int main(int argc, char const* argv[]) {
    // Program requires 2 argumets - Input and output file paths.
    if (argc != 3) {
        cout << "Provide the input file  and output file paths" << endl;
        return 0;
    }
    // Input file is considered as first argument
    string input_file = argv[1];
    // Output file is considered as second argument
    string output_file = argv[2];
    auto labrynth = read_labrynth(input_file);
    auto adjacency_list = get_adjacency_list(labrynth);
    // The first row having '.' is considered as an entrance
    auto entrances = get_entrances(labrynth[0]);
    // Find list of longest paths from each of possible entrances
    auto paths = find_longest_paths(adjacency_list, entrances);
    // Find the largest path among these
    vector<Node> longest_path;
    int longest_path_size = 0;
    for (auto path : paths) {
        if (path.size() > longest_path_size) {
            longest_path_size = path.size();
            longest_path = path;
        }
    }
    write_output(labrynth, longest_path, output_file);
    return 0;
}

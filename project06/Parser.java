public class Parser {
    public static void main(String args[]) {
        System.out.println("Hello Java");
    }
}


// Constructor receives a string with the filename
// boolean hasMoreCommands();
// void advance();
// Read one line at time. Skip whitespace and comments
// Differentiate the type of current command (C, A or label).
// Breaks into parts: .comp() .dest() .jump() (all of this one returns the string with the part)
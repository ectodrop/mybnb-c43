package com.mybnb;
import java.sql.*;


public class Main {
    public static void main(String[] args) throws Exception{
        Class.forName("com.mysql.cj.jdbc.Driver");
        String url = "jdbc:mysql://127.0.0.1/mybnb";
        Connection conn = DriverManager.getConnection(url, "root", "password1234");
        System.out.println("Connection successful");

        PreparedStatement execStat=conn.prepareStatement("SELECT * FROM Student");
        ResultSet rs = execStat.executeQuery();
        while (rs.next()) {
            int sid  = rs.getInt("sID");
            String fname = rs.getString("firstName");
            String lname = rs.getString("surName");
            System.out.println(sid + ": " + fname + " " + lname);
        }

    }
}
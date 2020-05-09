package lets_frontend;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Optional;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import com.google.gson.Gson;

import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.CheckBox;
import javafx.scene.control.PasswordField;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;
import javafx.scene.control.Alert.AlertType;
import javafx.event.EventHandler;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
import javafx.stage.Window;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.concurrent.Worker.State;
import javafx.event.ActionEvent;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.scene.control.ComboBox;

public class SignupOwnerController {
	@FXML
	TextField shopName;
	
	@FXML
	TextField ownerName;
	
	@FXML
	ComboBox shopType;
	
	@FXML
	TextField phone;
	
	@FXML
	TextField email;
	
	@FXML
	CheckBox mon;
	
	@FXML
	CheckBox tue;
	
	@FXML
	CheckBox wed;
	
	@FXML
	CheckBox thu;
	
	@FXML
	CheckBox fri;
	
	@FXML
	CheckBox sat;
	
	@FXML
	CheckBox sun;
	
	@FXML
	CheckBox b1;
	
	@FXML
	CheckBox b2;
	
	@FXML
	CheckBox b3;
	
	@FXML
	CheckBox b4;
	
	@FXML
	WebView map;
	
	@FXML
	TextField colony;
	
	@FXML
	TextField pinCode;
	
	@FXML
	TextField area;
	
	@FXML
	TextField city;
	
	@FXML
	TextField state;
	
	@FXML
	PasswordField password;
	
	@FXML
	PasswordField confirmPassword;
	
	@FXML
	CheckBox tick;
	
	@FXML
	Button submit;
	
	@FXML
	TextField code;
	
	@FXML
	Button confirm;
	
	@FXML
	Button back;
	
	@FXML
	public void initialize() {
		
		back.setOnAction(e -> {
			//go to login page
			try {
				System.out.println("go to login page");
				Parent loader = FXMLLoader.load(getClass().getResource("/fxml/login_page.fxml"));
				
				Scene scene = back.getScene();
				Window window = scene.getWindow();
				Stage stage = (Stage) window;
				
				back.getScene().setRoot(loader);
			}catch(Exception ee) {
				System.out.println("going to login page: " + ee);
			}
		});
		
		//map
		final WebEngine webEngine = map.getEngine();
		webEngine.load("https://www.google.com/maps/place/");
        
		mon.setSelected(true);
		tue.setSelected(true);
		wed.setSelected(true);
		thu.setSelected(true);
		fri.setSelected(true);
		sat.setSelected(true);
		sun.setSelected(true);
		
		shopType.getItems().addAll(
				"Antique Shop", "Bakery", "Barbershop", "Beauty Parlour", "Bookshop", "Booth", 
				"Bottle Shop", "Boutique", "Butcher", "Cafe", "Dairy", "Drugstore", "Garage", 
				"Hardware Shop", "Stationer", "Ration Shop"
		);
		
		
		submit.setOnAction(e -> {
			if(tick.isSelected() == true) {
				
				String strShopName = shopName.getText().trim();
				String strShopType = (String) shopType.getSelectionModel().getSelectedItem();
				String strOwnerName = ownerName.getText().trim();
				String strPhone = phone.getText().trim();
				String strEmail = email.getText().trim();
				
				String strMon = (mon.isSelected() == true)? "1" : "0";
				String strTue = (tue.isSelected() == true)? "1" : "0";
				String strWed = (wed.isSelected() == true)? "1" : "0";
				String strThu = (thu.isSelected() == true)? "1" : "0";
				String strFri = (fri.isSelected() == true)? "1" : "0";
				String strSat = (sat.isSelected() == true)? "1" : "0";
				String strSun = (sun.isSelected() == true)? "1" : "0";
				
				String strB1 = (b1.isSelected() == true)? "1" : "0";
				String strB2 = (b2.isSelected() == true)? "1" : "0";
				String strB3 = (b3.isSelected() == true)? "1" : "0";
				String strB4 = (b4.isSelected() == true)? "1" : "0";
				
				String strColony = colony.getText().trim();
				String strPin = pinCode.getText().trim();
				String strArea = area.getText().trim();
				String strCity = city.getText().trim();
				String strState = state.getText().trim();
				
				String strPassword = password.getText().trim();
				String strConfirmPassword = confirmPassword.getText().trim();
				
				if(strShopName.equalsIgnoreCase("") != true && strOwnerName.equalsIgnoreCase("") != true &&
					strPhone.equalsIgnoreCase("") != true && strEmail.equalsIgnoreCase("") != true &&
					strColony.equalsIgnoreCase("") != true && strPin.equalsIgnoreCase("") != true &&
					strArea.equalsIgnoreCase("") != true && strCity.equalsIgnoreCase("") != true &&
					strState.equalsIgnoreCase("") != true && strPassword.equalsIgnoreCase("") != true &&
					strConfirmPassword.equalsIgnoreCase("") != true) {
					
					//send to the server
					try {
						//connect
	            		URL url = new URL("http://127.0.0.1:5000" + 
        						"/signup/owner/" + strOwnerName.replace(" ", "%20") + "/"
        						+ strShopType.replace(" ", "%20") + "/" + strShopName.replace(" ", "%20")
        						+ "/" + 
        						strColony.replace(" ", "%20") + ",%20" + strArea.replace(" ", "%20") + ",%20"
        						+ strCity.replace(" ", "%20") + ",%20" + strState.replace(" ", "%20") + "%20"
        						+ strPin.replace(" ", "%20") + "/"
        						+ strPhone.replace(" ", "%20") + "/" + strEmail.replace(" ","%20") + "/" +
        						strPassword.replace(" ", "%20") + "/" + strConfirmPassword.replace(" ", "%20") +
        						"/" + strMon + "/" + strTue + "/" + strWed + "/" + strThu + "/" + strFri + "/"
        						 + strSat + "/" + strSun + "/" + strB1 + "/" + strB2 + "/" + strB3 + "/" +  strB4
	            				);
        				
        				HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        				conn.setRequestMethod("POST");
        				conn.setRequestProperty("Accept", "JSON");
        				
        				//storing JSON object in a string
        				BufferedReader br = new BufferedReader(new InputStreamReader(
        						(conn.getInputStream())));
        				String output,result = "";
        				while ((output = br.readLine()) != null) {
        					result += output.trim();
        				}
        				
        				System.out.println("Server Output: " + result);
        				
        				JSONParser parse = new JSONParser(); 
        				JSONObject jsonObject = (JSONObject)parse.parse(result);
	            		
        				if(jsonObject.get("message").toString().toLowerCase().equalsIgnoreCase("Verification code has been sent to your email address. Check your email and enter the code.")) {
        					Alert correct = new Alert(AlertType.INFORMATION);
        					correct.setTitle("Successful");
        					correct.setHeaderText("Account Registered");
        					correct.setContentText(jsonObject.get("message") + "\n\n\n");
        					correct.show();
        				}else {
        					Alert wrongCredentials = new Alert(AlertType.ERROR);
        					wrongCredentials.setTitle("Message");
        					wrongCredentials.setHeaderText("Signup Failed");
        					wrongCredentials.setContentText(jsonObject.get("message").toString()
    								+ "\n\n\n");
        					wrongCredentials.show();
        				}
					}catch(Exception ee) {
						Alert wrongCredentials = new Alert(AlertType.ERROR);
    					wrongCredentials.setTitle("Error");
    					wrongCredentials.setHeaderText("Sorry. Failed!");
    					wrongCredentials.setContentText("Cannot connect to the server. Please try again "
    							+ "after some time.\n\n\n");
    					wrongCredentials.show();
					}
				}else {
					Alert emptyFields = new Alert(AlertType.WARNING);
            		emptyFields.setTitle("Message");
            		emptyFields.setHeaderText("Field(s) found empty");
            		emptyFields.setContentText("Enter all the fields and try again.\n\n\n");
            		emptyFields.show();
				}
			}
		});
		
		confirm.setOnAction(e -> {
			if(code.getText().trim().equalsIgnoreCase("") != true) {
				try {
					//down
					URL url = new URL("http://127.0.0.1:5000" + 
							"/activate/owner/" + email.getText().replace(" ", "%20")
							+ "/" + code.getText().trim().replace(" ", "%20"));
					HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    				conn.setRequestMethod("POST");
    				conn.setRequestProperty("Accept", "JSON");
    				
    				//storing JSON object in a string
    				BufferedReader br = new BufferedReader(new InputStreamReader(
    						(conn.getInputStream())));
    				String output,result = "";
    				while ((output = br.readLine()) != null) {
    					result += output.trim();
    				}
    				
    				System.out.println("Server Output: " + result);
    				
    				JSONParser parse = new JSONParser(); 
    				JSONObject jsonObject = (JSONObject)parse.parse(result);
    				
    				if(jsonObject.get("message").toString().equalsIgnoreCase("True")) {
    					//verified
    					Alert correct = new Alert(AlertType.INFORMATION);
    					correct.setTitle("Successful");
    					correct.setHeaderText("Account Verified");
    					correct.setContentText("Your account has been verified. Enter your password to login. Press OK to continue."
    							+ "\n\n\n");
    					Optional<ButtonType> verified = correct.showAndWait();
    					if(verified.get() == ButtonType.OK) {
    						
    						//go to login page
    						try {
    		    				System.out.println("go to login page");
    		    				Parent loader = FXMLLoader.load(getClass().getResource("/fxml/login_page.fxml"));
    							
    							Scene scene = back.getScene();
    							Window window = scene.getWindow();
    							Stage stage = (Stage) window;
    							
    							back.getScene().setRoot(loader);
    		    			}catch(Exception ee) {
    		    				System.out.println("going to login page: " + ee);
    		    			}
    						
    					}
    				}else if(jsonObject.get("message").toString().equalsIgnoreCase("False")){
    					//incorrect otp
    					Alert incorrect = new Alert(AlertType.ERROR);
    					incorrect.setTitle("Failed");
    					incorrect.setHeaderText("Incorect Verification Code");
    					incorrect.setContentText("Entered verification code is incorrect. Please check your email and try again."
    							+ "\n\n\n");
    					incorrect.show();
    				}
					
					
					//up
				}catch(Exception ex) {
					Alert wrongCredentials = new Alert(AlertType.ERROR);
					wrongCredentials.setTitle("Error");
					wrongCredentials.setHeaderText("Sorry. Failed!");
					wrongCredentials.setContentText("Cannot connect to the server. Please try again "
							+ "after some time.\n\n\n");
					wrongCredentials.show();
				}
			}
		});
	}
}

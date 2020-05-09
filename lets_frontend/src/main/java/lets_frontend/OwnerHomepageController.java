package lets_frontend;

import javafx.application.Application;

import java.io.*;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;

import java.util.regex.Pattern;

import javafx.scene.control.cell.PropertyValueFactory;
import javafx.beans.property.SimpleStringProperty;
import javafx.geometry.Insets;
import javafx.scene.Group;
import javafx.scene.Parent;

import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.event.MouseEvent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.stage.Window;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;
import javafx.scene.paint.Color;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.collections.*;
import javafx.scene.effect.*;
import javafx.scene.control.Alert.AlertType;

import java.text.DateFormat;
import java.util.*;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

import javafx.geometry.Orientation;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.awt.Desktop;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;

import org.apache.commons.lang3.text.WordUtils;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import java.text.SimpleDateFormat;
import java.util.Date;


public class OwnerHomepageController {
	
	@FXML
	Button aboutApp;
	
	@FXML
	Button refresh;
	
	@FXML
	Button deactivateAccount;
	
	@FXML
	Button logout;
	
	@FXML
	VBox complaintBox;
	
	@FXML
	HBox customerBox;
	
	@FXML
	Label today;
	
	@FXML
	HBox todayBatchBox;
	
	@FXML
	HBox otherBatchBox;
	
	@FXML
	HBox shopBox;
	
	@FXML
	RadioButton shopAll;
	
	@FXML
	RadioButton shopSameCategory;
	
	@FXML
	RadioButton myBatch;
	
	ToggleGroup shop = new ToggleGroup();
	
	@FXML
	Label shopId;
	
	@FXML
	Label email;
	
	@FXML
	TextField shopName;
	
	@FXML
	TextField ownerName;
	
	@FXML
	ComboBox shopType;
	
	@FXML
	TextArea address;
	
	@FXML
	TextField phone;
	
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
	Button save;
	
	@FXML
	RadioButton past;
	
	@FXML
	RadioButton future;
	
	@FXML
	Button batch;
	
	ToggleGroup batchToggle = new ToggleGroup();
	
	TableView customerTable = new TableView();
	TableColumn<String , CustomerClass> customerCol1 = new TableColumn<>("Name");
	
	TableView todayBatchTable = new TableView();
	TableColumn<String , TodayBatchClass> todayBatchCol1 = new TableColumn<>("Batch");
	TableColumn<String , TodayBatchClass> todayBatchCol2 = new TableColumn<>("Opening Time");
	TableColumn<String , TodayBatchClass> todayBatchCol3 = new TableColumn<>("Closing Time");
	
	TableView futurePastBatchTable = new TableView();
	TableColumn<String , FuturePastBatchClass> futurePastCol1 = new TableColumn<>("Day");
	TableColumn<String , FuturePastBatchClass> futurePastCol2 = new TableColumn<>("Batch");
	TableColumn<String , FuturePastBatchClass> futurePastCol3 = new TableColumn<>("Opening Time");
	TableColumn<String , FuturePastBatchClass> futurePastCol4 = new TableColumn<>("Closing Time");
	
	
	@FXML
	public void initialize() {
		
		batch.setOnAction(e -> {
			Alert about = new Alert(AlertType.INFORMATION);
			
			
			about.setTitle("Details");
			about.setHeaderText("Batch Timings");
			about.setContentText("\nBatch 1: 6:00 AM to 10:00 AM\n\n" + 
								 "Batch 2: 10:00 AM to 2:00 PM\n\n" + 
								 "Batch 3: 2:00 PM to 6:00 PM\n\n" +
								 "Batch 4: 6:00 PM to 10:00 PM\n\n\n");
			
			about.show();
		});
		
		shopAll.setToggleGroup(shop);
		shopSameCategory.setToggleGroup(shop);
		myBatch.setToggleGroup(shop);
		shopAll.setSelected(true);
		
		shopAll.setOnAction(e -> {
			loadShops("nearby/shops/all_category/");
		});
		shopSameCategory.setOnAction(e -> {
			loadShops("nearby/shops/same_category/");
		});
		myBatch.setOnAction(e -> {
			loadShops("same_batch/");
		});
		
		future.setToggleGroup(batchToggle);
		past.setToggleGroup(batchToggle);
		future.setSelected(true);
		
		future.setOnAction(e -> {
			loadOtherBatches("future");
		});
		past.setOnAction(e -> {
			loadOtherBatches("past");
		});
		
		
		customerTable.setStyle("-fx-border-color: '#808080';" + "-fx-border-width: 1px;");
		customerCol1.setCellValueFactory(new PropertyValueFactory<>("name"));
		customerCol1.setMinWidth(230.0);
		customerCol1.setMaxWidth(300.0);
		customerTable.getColumns().addAll(customerCol1);
		
		customerBox.getChildren().add(customerTable);
		
		todayBatchTable.setStyle("-fx-border-color: '#808080';" + "-fx-border-width: 1px;");
		todayBatchCol1.setCellValueFactory(new PropertyValueFactory<>("batch"));
		todayBatchCol1.setMinWidth(130.0);
		todayBatchCol1.setMaxWidth(130.0);
		todayBatchCol2.setCellValueFactory(new PropertyValueFactory<>("openingTime"));
		todayBatchCol2.setMinWidth(158.0);
		todayBatchCol2.setMaxWidth(158.0);
		todayBatchCol3.setCellValueFactory(new PropertyValueFactory<>("closingTime"));
		todayBatchCol3.setMinWidth(158.0);
		todayBatchCol3.setMaxWidth(158.0);
		todayBatchTable.getColumns().addAll(todayBatchCol1, todayBatchCol2, todayBatchCol3);
		
		todayBatchBox.getChildren().add(todayBatchTable);
		
		futurePastBatchTable.setStyle("-fx-border-color: '#808080';" + "-fx-border-width: 1px;");
		futurePastCol1.setCellValueFactory(new PropertyValueFactory<>("day"));
		futurePastCol1.setMinWidth(150.0);
		futurePastCol2.setCellValueFactory(new PropertyValueFactory<>("batch"));
		futurePastCol2.setMinWidth(86.0);
		futurePastCol2.setMaxWidth(86.0);
		futurePastCol3.setCellValueFactory(new PropertyValueFactory<>("openingTime"));
		futurePastCol3.setMinWidth(105.0);
		futurePastCol3.setMaxWidth(105.0);
		futurePastCol4.setCellValueFactory(new PropertyValueFactory<>("closingTime"));
		futurePastCol4.setMinWidth(105.0);
		futurePastCol4.setMaxWidth(105.0);
		futurePastBatchTable.getColumns().addAll(futurePastCol1, futurePastCol2, futurePastCol3,
				futurePastCol4);
		
		otherBatchBox.getChildren().add(futurePastBatchTable);
		
		refresh();
		
		shopType.getItems().addAll(
				"Antique Shop", "Bakery", "Barbershop", "Beauty Parlour", "Bookshop", "Booth", 
				"Bottle Shop", "Boutique", "Butcher", "Cafe", "Dairy", "Drugstore", "Garage", 
				"Hardware Shop", "Stationer", "Ration Shop"
		);
		
		aboutApp.setOnAction(e -> {
			aboutApp();
		});
		
		logout.setOnAction(e -> {
			Alert ask = new Alert(AlertType.CONFIRMATION);
        	ask.setTitle("Confirmation");
        	ask.setHeaderText("Do you want to logout?");
        	ask.setContentText("Are you sure? Press OK to continue."
					+ "\n\n\n");
        	Optional<ButtonType> answer = ask.showAndWait();
        	if(answer.get() == ButtonType.OK) {
        		try {
					Parent loader = FXMLLoader.load(getClass().getResource("/fxml/login_page.fxml"));
					
					Scene scene = logout.getScene();
					Window window = scene.getWindow();
					Stage stage = (Stage) window;
					
					logout.getScene().setRoot(loader);
					
				}catch(Exception exp) {
					System.out.println("Going to LoginPage: " + exp);
				}
        	}
		});
		
		refresh.setOnAction(e -> {
			refresh();
		});
		
		save.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
            	if(email.getText().trim().toLowerCase().equalsIgnoreCase("") != true && 
            			ownerName.getText().trim().toLowerCase().equalsIgnoreCase("") != true && 
            			shopType.getSelectionModel().getSelectedItem().toString().trim().toLowerCase().equalsIgnoreCase("") != true && 
            			shopName.getText().trim().toLowerCase().equalsIgnoreCase("") != true && 
            			address.getText().trim().toLowerCase().equalsIgnoreCase("") != true && 
            			phone.getText().trim().toLowerCase().equalsIgnoreCase("") != true) {
            		
            		//confirmation
            		Alert ask = new Alert(AlertType.CONFIRMATION);
            		ask.setTitle("Confirmation");
            		ask.setHeaderText("Update Account?");
            		ask.setContentText("Are you sure? If yes then press OK else press Cancel.\n\n\n");
            		Optional<ButtonType> what = ask.showAndWait();
            		if(what.get() == ButtonType.OK) {
                		int MON = (mon.isSelected())?1:0;
                		int TUE = (tue.isSelected())?1:0;
                		int WED = (wed.isSelected())?1:0;
                		int THU = (thu.isSelected())?1:0;
                		int FRI = (fri.isSelected())?1:0;
                		int SAT = (sat.isSelected())?1:0;
                		int SUN = (sun.isSelected())?1:0;
                		
                		int B1 = (b1.isSelected())?1:0;
                		int B2 = (b2.isSelected())?1:0;
                		int B3 = (b3.isSelected())?1:0;
                		int B4 = (b4.isSelected())?1:0;
                		
            			updateInfo(
                				email.getText(), ownerName.getText(), shopType.getSelectionModel().getSelectedItem().toString(),
                				shopName.getText(), address.getText(), phone.getText(),
                				MON, TUE, WED, THU, FRI, SAT, SUN, B1, B2, B3, B4
                		);
                	}else {
            			//update saved info
            			loadOwnerDetails();
            		}
            	}else {
            		Alert empty = new Alert(AlertType.ERROR);
            		empty.setTitle("Error");
            		empty.setHeaderText("Cannot Update!");
            		empty.setContentText("Some field(s) is/are found empty. "
            				+ "Please enter all the fields and try again.\n\n\n");
            		empty.show();
            	}
            }});
		
	}
	
	public void updateInfo(String email, String ownerName, String shopType,String shopName, String address, 
			String phone, int MON, int TUE, int WED, int THU, int FRI, int SAT, int SUN, int B1, 
			int B2, int B3, int B4) {
		email = email.trim().replace(" ", "%20");
		ownerName = ownerName.trim().replace(" ", "%20");
		shopType = shopType.trim().replace(" ", "%20");
		shopName = shopName.trim().replace(" ", "%20");
		address = address.trim().replace(" ", "%20");
		phone = phone.trim().replace(" ", "%20");
		
		try {
			//connection
			URL url = new URL("http://127.0.0.1:5000/update/owner/"
					+ email + "/" + ownerName + "/" + shopType + "/" + shopName + "/" + 
							address + "/" + phone + "/" + MON + "/" + TUE + "/" + WED + "/" + THU + "/" +
					FRI + "/" + SAT + "/" + SUN + "/" + B1 + "/" + B2 + "/" + B3 + "/" + B4);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("PUT");
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
			
			String isDone = jsonObject.get("message").toString();
			if(isDone.equalsIgnoreCase("True")) {
				Alert wrongCredentials = new Alert(AlertType.INFORMATION);
    			wrongCredentials.setTitle("Successful");
    			wrongCredentials.setHeaderText("Account Updated");
    			wrongCredentials.setContentText(
    							"Your account details has been updated. Press OK to continue." + 
    							"\n\n\n");
    			wrongCredentials.show();
			}else {
				Alert wrongCredentials = new Alert(AlertType.ERROR);
    			wrongCredentials.setTitle("Filed");
    			wrongCredentials.setHeaderText("Account not updated");
    			wrongCredentials.setContentText(
    					isDone + 
    					"\n\n\n");
    			wrongCredentials.show();
			}
			
		}catch(Exception error) {
			System.out.println("updateInfo: " + error);
		}finally {
			//fetch latest user-information
			loadOwnerDetails();
		}
	}
	
	public void loadOtherBatches(String tense) {
		try {
			String addr = address.getText().trim().toLowerCase().replace(" ", "%20");
			//connecting
			URL url = new URL("http://127.0.0.1:5000/batch/" + tense + "/" + Index.connectedEmail);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "JSON");
		
			//storing JSON object in a string
			BufferedReader br = new BufferedReader(new InputStreamReader(
					(conn.getInputStream())));
			String output,result = "";
			while ((output = br.readLine()) != null) {
				result += output.trim();
			}
			result = "{\"results\" : " + result + " }";
			System.out.println("Today's batches...");
			System.out.println("Server Output: " + result);
		
			JSONParser parse = new JSONParser();
			System.out.println(0);
			
			System.out.println(result);
			JSONObject jsonObject = (JSONObject)parse.parse(result);
			System.out.println(1);
			JSONArray customerArray = (JSONArray) jsonObject.get("results");
			System.out.println("till here");
			
			futurePastBatchTable.getItems().clear();
			for(int i = 0 ; i < customerArray.size() ; i++)
			{
				System.out.println("indise futurePast...(loadOtherBatches) loop");
				JSONObject arrayElement =  (JSONObject)customerArray.get(i);
				
				String element1 = arrayElement.get("date").toString();
				String element3 = arrayElement.get("incoming_time").toString();
				String element4 = arrayElement.get("outgoing_time").toString();
				
				element3 = element3.substring(0, 5) + " " + element3.substring(9);
				element4 = element4.substring(0, 5) + " " + element4.substring(9);
				
				String element2 = "";
				
				if(element3.equalsIgnoreCase("06:00:00 AM"))
					element2 = "Batch 1";
				else if (element3.equalsIgnoreCase("10:00 AM"))
					element2 = "Batch 2";
				else if (element3.equalsIgnoreCase("02:00 PM"))
					element2 = "Batch 3";
				else
					element2 = "Batch 4";
				
				//populating todayBatch table
				futurePastBatchTable.getItems().add(new FuturePastBatchClass(element1, element2, element3,
						element4));
			}
			
			
		}catch(Exception e) {
			System.out.println("Error while loading futurePast batches:\n" + e);
		}
	}
	
	public void refresh() {
		//today
		SimpleDateFormat sdf = new SimpleDateFormat("%d MM yyyy");
		Date d = new Date();
		today.setText(sdf.format(d).toString());
		
		// fill homepage with data
		
		//get shop details
		loadOwnerDetails();
		
		//load customers
		try {
			String addr = address.getText().trim().toLowerCase().replace(" ", "%20");
			//connecting
			URL url = new URL("http://127.0.0.1:5000/nearby/customers/" + addr);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "JSON");
		
			//storing JSON object in a string
			BufferedReader br = new BufferedReader(new InputStreamReader(
					(conn.getInputStream())));
			String output,result = "";
			while ((output = br.readLine()) != null) {
				result += output.trim();
			}
			result = "{\"results\" : " + result + " }";
			System.out.println("Customer...");
			System.out.println("Server Output: " + result);
		
			JSONParser parse = new JSONParser();
			System.out.println(0);
			
			System.out.println(result);
			JSONObject jsonObject = (JSONObject)parse.parse(result);
			System.out.println(1);
			JSONArray customerArray = (JSONArray) jsonObject.get("results");
			System.out.println("till here");
			
			customerTable.getItems().clear();
			for(int i = 0 ; i < customerArray.size() ; i++)
			{
				JSONObject arrayElement =  (JSONObject)customerArray.get(i);
				
				String element = WordUtils.capitalizeFully(arrayElement.get("name").toString(), delimiters);
				System.out.println(element);
				
				//populating customer's table
				customerTable.getItems().add(new CustomerClass(element));
			}
			
			
		}catch(Exception e) {
			System.out.println("Error while loading customers:\n" + e);
		}
		
		//load today batches
		try {
			String addr = address.getText().trim().toLowerCase().replace(" ", "%20");
			//connecting
			URL url = new URL("http://127.0.0.1:5000/batch/present/" + Index.connectedEmail);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "JSON");
		
			//storing JSON object in a string
			BufferedReader br = new BufferedReader(new InputStreamReader(
					(conn.getInputStream())));
			String output,result = "";
			while ((output = br.readLine()) != null) {
				result += output.trim();
			}
			result = "{\"results\" : " + result + " }";
			System.out.println("Today's batches...");
			System.out.println("Server Output: " + result);
		
			JSONParser parse = new JSONParser();
			System.out.println(0);
			
			System.out.println(result);
			JSONObject jsonObject = (JSONObject)parse.parse(result);
			System.out.println(1);
			JSONArray customerArray = (JSONArray) jsonObject.get("results");
			System.out.println("till here");
			
			todayBatchTable.getItems().clear();
			for(int i = 0 ; i < customerArray.size() ; i++)
			{
				JSONObject arrayElement =  (JSONObject)customerArray.get(i);
				
				String element1 = arrayElement.get("incoming_time").toString();
				String element2 = arrayElement.get("outgoing_time").toString();
				System.out.println(element1 + "\t" + element2);
				
				element1 = element1.substring(0, 5) + " " + element1.substring(9);
				element2 = element2.substring(0, 5) + " " + element2.substring(9);
				
				String element0 = "";
				
				if(element1.equalsIgnoreCase("06:00:00 AM"))
					element0 = "Batch 1";
				else if (element1.equalsIgnoreCase("10:00 AM"))
					element0 = "Batch 2";
				else if (element1.equalsIgnoreCase("02:00 PM"))
					element0 = "Batch 3";
				else
					element0 = "Batch 4";
				
				//populating todayBatch table
				todayBatchTable.getItems().add(new TodayBatchClass(element0, element1, element2));
			}
			
			
		}catch(Exception e) {
			System.out.println("Error while loading today's batches:\n" + e);
		}
		
		//load other batches: futurePast
		if(future.isSelected())
			loadOtherBatches("future");
		else
			loadOtherBatches("past");
		
		//load shops
		if(shopAll.isSelected())
			loadShops("nearby/shops/all_category/");
		else if(shopSameCategory.isSelected())
			loadShops("nearby/shops/same_category/<string:shopType>/");
		else	//my batch
			loadShops("same_batch/");
		
		//load complaints
		loadComplaints();
		
	}
	
	public void loadComplaints() {
		try {
			System.out.println("loading complaints...");
			//connecting
			URL url = new URL("http://127.0.0.1:5000/complaint/get/" + Index.connectedEmail);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "JSON");
		
			//storing JSON object in a string
			BufferedReader br = new BufferedReader(new InputStreamReader(
					(conn.getInputStream())));
			String output,result = "";
			while ((output = br.readLine()) != null) {
				result += output.trim();
			}
			result = "{\"results\" : " + result + " }";
			JSONParser parse = new JSONParser();
			System.out.println(result);
			JSONObject jsonObject = (JSONObject)parse.parse(result);
			JSONArray customerArray = (JSONArray) jsonObject.get("results");
			
			//futurePastBatchTable.getItems().clear();
			for(int i = 0 ; i < customerArray.size() ; i++)
			{
				JSONObject arrayElement =  (JSONObject)customerArray.get(i);
				
				String element1 = WordUtils.capitalizeFully(arrayElement.get("date").toString(), delimiters);
				String element2 = arrayElement.get("time").toString();
				String element3 = arrayElement.get("reason").toString();
					
				//populating todayBatch table
				//TODO
				
				//printing
				System.out.println("> " + element1 + "\t" + element2 + "\t" + element3);
				
			}
			
			
		}catch(Exception e) {
			System.out.println("Error while loading complaints:\n" + e);
		}
		}
	
	public void loadShops(String addressURL) {
		//for same batch: send email
		// others: send address
		String urlTail = "";
		if(shopAll.isSelected())
			urlTail = address.getText().trim().toLowerCase().replace(" ", "%20");
		else if(shopSameCategory.isSelected())
			urlTail = shopType.getSelectionModel().getSelectedItem().toString().trim().replace(" ", "%20")
						+ "/" + address.getText().trim().toLowerCase().replace(" ", "%20");
		else
			urlTail = Index.connectedEmail.trim().toLowerCase().replace(" ", "%20");
		
		try {
			System.out.println("Loading shops...");
			//connecting
			URL url = new URL("http://127.0.0.1:5000/" + addressURL + urlTail);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "JSON");
		
			//storing JSON object in a string
			BufferedReader br = new BufferedReader(new InputStreamReader(
					(conn.getInputStream())));
			String output,result = "";
			while ((output = br.readLine()) != null) {
				result += output.trim();
			}
			result = "{\"results\" : " + result + " }";
			System.out.println("Other nearby shops...");
			System.out.println("Server Output: " + result);
		
			JSONParser parse = new JSONParser();
			System.out.println(0);
			
			System.out.println(result);
			JSONObject jsonObject = (JSONObject)parse.parse(result);
			System.out.println(1);
			JSONArray customerArray = (JSONArray) jsonObject.get("results");
			System.out.println("till here");
			
			//futurePastBatchTable.getItems().clear();
			for(int i = 0 ; i < customerArray.size() ; i++)
			{
				System.out.println("inside other shops...(loadShops) loop");
				JSONObject arrayElement =  (JSONObject)customerArray.get(i);
				
				if(arrayElement.get("email").toString().equalsIgnoreCase(Index.connectedEmail) != true) {
					String element1 = arrayElement.get("shop_id").toString();
					String element2 = arrayElement.get("name").toString();
					String element3 = arrayElement.get("shop_name").toString();
					
					//populating todayBatch table
					//TODO
					//printing
					System.out.println("> " + element1 + "\t" + element2 + "\t" + element3);
				}
			}
			
			
		}catch(Exception e) {
			System.out.println("Error occured while loading shops:\n" + e);
		}
		
		
	}
	
	final char[] delimiters = { ' ', '_' };
	
	@SuppressWarnings("deprecation")
	public void loadOwnerDetails() {
		try {
			//connecting
			URL url = new URL("http://127.0.0.1:5000/shop/details/" + Index.connectedEmail);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
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
			
			//loading shop details
			shopId.setText(WordUtils.capitalizeFully(jsonObject.get("shop_id").toString(), delimiters));
			email.setText(Index.connectedEmail);
			shopName.setText(WordUtils.capitalizeFully(jsonObject.get("shop_name").toString(), delimiters));
			ownerName.setText(WordUtils.capitalizeFully(jsonObject.get("name").toString(), delimiters));
			phone.setText(jsonObject.get("phone").toString());
			address.setText(WordUtils.capitalizeFully(jsonObject.get("address").toString(), delimiters));
			address.setWrapText(true);
			
			shopType.setValue(WordUtils.capitalizeFully(jsonObject.get("type").toString(), delimiters));
			
			if(jsonObject.get("mon").toString().equalsIgnoreCase("1"))
				mon.setSelected(true);
			else
				mon.setSelected(false);
			if(jsonObject.get("tue").toString().equalsIgnoreCase("1"))
				tue.setSelected(true);
			else
				tue.setSelected(false);
			if(jsonObject.get("wed").toString().equalsIgnoreCase("1"))
				wed.setSelected(true);
			else
				wed.setSelected(false);
			if(jsonObject.get("thu").toString().equalsIgnoreCase("1"))
				thu.setSelected(true);
			else
				thu.setSelected(false);
			if(jsonObject.get("fri").toString().equalsIgnoreCase("1"))
				fri.setSelected(true);
			else
				fri.setSelected(false);
			if(jsonObject.get("sat").toString().equalsIgnoreCase("1"))
				sat.setSelected(true);
			else
				sat.setSelected(false);
			if(jsonObject.get("sun").toString().equalsIgnoreCase("1"))
				sun.setSelected(true);
			else
				sun.setSelected(false);
			if(jsonObject.get("batch1").toString().equalsIgnoreCase("1"))
				b1.setSelected(true);
			else
				b1.setSelected(false);
			if(jsonObject.get("batch2").toString().equalsIgnoreCase("1"))
				b2.setSelected(true);
			else
				b2.setSelected(false);
			if(jsonObject.get("batch3").toString().equalsIgnoreCase("1"))
				b3.setSelected(true);
			else
				b3.setSelected(false);
			if(jsonObject.get("batch4").toString().equalsIgnoreCase("1"))
				b4.setSelected(true);
			else
				b4.setSelected(false);
			
		}catch(Exception err) {
			System.out.println("LoadingHomepage: " + err);
			
			Alert wrongCredentials = new Alert(AlertType.ERROR);
			wrongCredentials.setTitle("Error");
			wrongCredentials.setHeaderText("Sorry. Failed!");
			wrongCredentials.setContentText("Cannot connect to the server. Please try again "
					+ "after some time.\n\n\n");
			wrongCredentials.show();
		}
	}
	
	public void aboutApp() {
		try {
			//connection
			URL url = new URL("http://127.0.0.1:5000/about");
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("Accept", "JSON");
		
			//storing JSON object in a string
			BufferedReader br = new BufferedReader(new InputStreamReader(
					(conn.getInputStream())));
			String output,result = "";
			while ((output = br.readLine()) != null) {
				result += output.trim();
			}
			result = result.replace("*", "\n");
			JSONParser parse = new JSONParser(); 
			JSONObject jsonObject = (JSONObject)parse.parse(result);
			
			String aboutData = jsonObject.get("message").toString();
			Alert about = new Alert(AlertType.INFORMATION);
			
			
			about.setTitle("About App");
			about.setHeaderText("Endure");
			about.setContentText(
					aboutData);
			about.getDialogPane().setMinWidth(800.0);
			about.show();
			
			
		}catch(Exception e) {
			System.out.println("aboutApp: " + e);
		}
	}
}

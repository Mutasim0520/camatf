/*
 * This is an example test project created in Eclipse to test NotePad which is a sample 
 * project located in AndroidSDK/samples/android-11/NotePad
 * 
 * 
 * You can run these test cases either on the emulator or on device. Right click
 * the test project and select Run As --> Run As Android JUnit Test
 * 
 * @author Renas Reda, renas.reda@robotium.com
 * 
 */

package com.example.android.notepad;

import com.robotium.solo.Solo;
import com.example.android.notepad.NotesList;
import com.robotium.solo.SystemUtils;

import android.app.Instrumentation;
import android.test.ActivityInstrumentationTestCase2;

import java.io.InputStreamReader;


public class NotePadTest extends ActivityInstrumentationTestCase2<NotesList> {

    private Solo solo;

    public NotePadTest() {
        super(NotesList.class);

    }

    @Override
    public void setUp() throws Exception {
        //setUp() is run before a test case is started.
        //This is where the solo object is created.
        solo = new Solo(getInstrumentation(), getActivity());
    }

    @Override
    public void tearDown() throws Exception {
        //tearDown() is run after a test case has finished.
        //finishOpenedActivities() will finish all the activities that have been opened during the test execution.
        String pretty = null;
        pretty = Instrumentation.REPORT_KEY_STREAMRESULT;
        pretty =  solo.toString();
        System.out.println("asdf"+pretty);
        solo.finishOpenedActivities();
    }


    public void testInternetCall() throws Exception {
        //Unlock the lock screen
        for (int i = 0; i < 1; i++) {
            solo.unlockScreen();
            solo.takeScreenshot();
            solo.clickOnMenuItem("Check Update");
            solo.takeScreenshot();
            //Assert that NoteEditor activity is opened
            solo.assertCurrentActivity("Expected NoteEditor activity", "ServiceCallActivity");
            //solo.waitForDialogToClose();
            solo.clickOnButton("OK");
            solo.takeScreenshot();
            Thread.sleep(2000);
            solo.goBack();
        }

    }

    public void testAddNote() throws Exception {
        //Unlock the lock screen
        solo.unlockScreen();
        solo.clickOnMenuItem("Add note");
        //Assert that NoteEditor activity is opened
        solo.assertCurrentActivity("Expected NoteEditor activity", "NoteEditor");
        //In text field 0, enter Note 1
        solo.enterText(0, "Note 1");
        solo.goBack();
        //Clicks on menu item
        solo.clickOnMenuItem("Add note");
        //In text field 0, type Note 2
        solo.typeText(0, "Note 2");
        //Go back to first activity
        solo.goBack();
        //Takes a screenshot and saves it in "/sdcard/Robotium-Screenshots/".
        solo.takeScreenshot();
        boolean notesFound = solo.searchText("Note 1") && solo.searchText("Note 2");
        //Assert that Note 1 & Note 2 are found
        assertTrue("Note 1 and/or Note 2 are not found", notesFound);
    }

    public void testEditNote() throws Exception {

        solo.clickLongInList(2);

        solo.clickOnText("Edit title");

        solo.hideSoftKeyboard();

        //solo.setActivityOrientation(Solo.LANDSCAPE);

        solo.enterText(0, " test");
        //solo.setActivityOrientation(Solo.PORTRAIT);

        boolean noteFound = solo.waitForText("(?i).*?note 1 test");

        assertTrue("Note 1 test is not found", noteFound);
    }





}
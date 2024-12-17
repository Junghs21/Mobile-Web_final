package com.example.mymwapplication;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class EmailVerificationActivity extends AppCompatActivity {

    private EditText etName, etEmail, etVerificationCode;
    private Button btnSendCode, btnVerifyCode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_email_verification);

        etName = findViewById(R.id.et_name);
        etEmail = findViewById(R.id.et_email);
        etVerificationCode = findViewById(R.id.et_verification_code);
        btnSendCode = findViewById(R.id.btn_send_code);
        btnVerifyCode = findViewById(R.id.btn_verify_code);

        // 인증번호 발송 버튼
        btnSendCode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String name = etName.getText().toString();
                String email = etEmail.getText().toString();

                if (!name.isEmpty() && !email.isEmpty()) {
                    new SendVerificationCodeTask().execute(name, email);

                    // 인증번호 입력 필드와 확인 버튼을 보이게 함
                    etVerificationCode.setVisibility(View.VISIBLE);
                    btnVerifyCode.setVisibility(View.VISIBLE);
                } else {
                    Toast.makeText(EmailVerificationActivity.this, "이름과 이메일을 입력하세요.", Toast.LENGTH_SHORT).show();
                }
            }
        });

        // 인증번호 확인 버튼
        btnVerifyCode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String email = etEmail.getText().toString();
                String code = etVerificationCode.getText().toString();

                if (!email.isEmpty() && !code.isEmpty()) {
                    new VerifyCodeTask().execute(email, code);
                } else {
                    Toast.makeText(EmailVerificationActivity.this, "이메일과 인증번호를 입력하세요.", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    // 인증번호 발송 Task
    private class SendVerificationCodeTask extends AsyncTask<String, Void, Boolean> {
        @Override
        protected Boolean doInBackground(String... params) {
            String name = params[0];
            String email = params[1];
            OkHttpClient client = new OkHttpClient();

            try {
                JSONObject json = new JSONObject();
                json.put("name", name);
                json.put("email", email);

                RequestBody body = RequestBody.create(json.toString(), MediaType.parse("application/json"));
                Request request = new Request.Builder()
                        .url("http://10.0.2.2:8000/api_root/email/send/")
                        .post(body)
                        .build();

                Response response = client.newCall(request).execute();
                return response.isSuccessful();

            } catch (Exception e) {
                e.printStackTrace();
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean success) {
            if (success) {
                Toast.makeText(EmailVerificationActivity.this, "인증번호 발송 성공", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(EmailVerificationActivity.this, "인증번호 발송 실패", Toast.LENGTH_SHORT).show();
            }
        }
    }

    // 인증번호 확인 Task
    private class VerifyCodeTask extends AsyncTask<String, Void, Boolean> {
        private String email;

        @Override
        protected Boolean doInBackground(String... params) {
            email = params[0];
            String code = params[1];
            OkHttpClient client = new OkHttpClient();

            try {
                JSONObject json = new JSONObject();
                json.put("email", email);
                json.put("code", code);

                RequestBody body = RequestBody.create(json.toString(), MediaType.parse("application/json"));
                Request request = new Request.Builder()
                        .url("http://10.0.2.2:8000/api_root/email/verify/")
                        .post(body)
                        .build();

                Response response = client.newCall(request).execute();
                return response.isSuccessful();

            } catch (Exception e) {
                e.printStackTrace();
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean success) {
            if (success) {
                Toast.makeText(EmailVerificationActivity.this, "인증 성공!", Toast.LENGTH_SHORT).show();

                // ImageUploadActivity로 이메일 값 전달
                Intent intent = new Intent(EmailVerificationActivity.this, ImageUploadActivity.class);
                intent.putExtra("email", email);  // 이메일 값을 추가
                startActivity(intent);
                finish();
            } else {
                Toast.makeText(EmailVerificationActivity.this, "인증 실패! 올바른 코드를 입력해주세요.", Toast.LENGTH_SHORT).show();
            }
        }
    }
}

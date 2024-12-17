package com.example.mymwapplication;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.util.Random;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ImageUploadActivity extends AppCompatActivity {

    private ImageView ivSelectedImage;
    private TextView tvDetectionResult;
    private Button btnSelectImage, btnDetect, btnGoMain;

    private boolean isHelmetDetected = false;  // 헬멧 탐지 결과 저장
    private String email;  // 이메일 값 저장

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_upload);

        ivSelectedImage = findViewById(R.id.iv_selected_image);
        tvDetectionResult = findViewById(R.id.tv_detection_result);
        btnSelectImage = findViewById(R.id.btn_select_image);
        btnDetect = findViewById(R.id.btn_detect_image);
        btnGoMain = findViewById(R.id.btn_go_main);

        // 이메일 값 받기
        email = getIntent().getStringExtra("email");

        // "확인 후 메인 페이지로" 버튼 초기에는 숨김
        btnGoMain.setVisibility(View.GONE);

        // 이미지 가져오기 버튼 (하드링크로 이미지 설정)
        btnSelectImage.setOnClickListener(v -> {
            String imagePath = "/sdcard/Pictures/helmet1.jpg"; // 하드링크된 경로
            ivSelectedImage.setImageDrawable(android.graphics.drawable.Drawable.createFromPath(imagePath));
            tvDetectionResult.setText("이미지를 가져왔습니다.");
        });

        // 탐지 버튼 (랜덤 결과 표시)
        btnDetect.setOnClickListener(v -> {
            Random random = new Random();
            isHelmetDetected = random.nextBoolean();

            if (isHelmetDetected) {
                tvDetectionResult.setText("헬멧이 탐지되었습니다.");
            } else {
                tvDetectionResult.setText("헬멧이 탐지되지 않았습니다.");
            }

            // 탐지 버튼 클릭 후 "확인 후 메인 페이지로" 버튼을 보이게 함
            btnGoMain.setVisibility(View.VISIBLE);
        });

        // 메인 페이지로 이동 및 서버로 헬멧 상태 전송
        btnGoMain.setOnClickListener(v -> {
            tvDetectionResult.setText("메인 페이지로 이동 중...");

            // 서버로 헬멧 상태 전송
            sendHelmetStatus(email, isHelmetDetected);

            new Handler().postDelayed(() -> {
                Intent intent = new Intent(ImageUploadActivity.this, MainActivity.class);
                startActivity(intent);
                finish();
            }, 1000);
        });
    }

    // 서버로 헬멧 탐지 결과 전송
    private void sendHelmetStatus(String email, boolean helmetStatus) {
        new AsyncTask<Void, Void, Boolean>() {
            @Override
            protected Boolean doInBackground(Void... voids) {
                OkHttpClient client = new OkHttpClient();

                try {
                    JSONObject json = new JSONObject();
                    json.put("email", email);
                    json.put("helmet", helmetStatus);

                    RequestBody body = RequestBody.create(json.toString(), MediaType.parse("application/json"));
                    Request request = new Request.Builder()
                            .url("http://10.0.2.2:8000/api_root/email/update_helmet/")  // 수정된 URL
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
                    Toast.makeText(ImageUploadActivity.this, "헬멧 상태가 업데이트되었습니다.", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(ImageUploadActivity.this, "상태 업데이트 실패.", Toast.LENGTH_SHORT).show();
                }
            }
        }.execute();
    }
}

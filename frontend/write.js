const form = document.getElementById("write-form"); // html에서 지정한 id로 가지고 오기 = form

const handleSubmitForm = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", Date.now().toString());
  try {
    const res = await fetch("/items", {
      method: "POST", //main.py에서 어떻게 썼는지 확인
      body, // javaScript 내장 객체 중 FormData 형식으로 form 값을 넣어서 보냄
    });
    const data = await res.json(); // res를 json으로 바꾸는 과정 필요
    // 제출 완료하면 메인 페이지(루트 경로)로 되돌아오도록
    if (data === "200") window.location.pathname = "/";
  } catch (error) {
    console.error(error);
  }
};

form.addEventListener("submit", handleSubmitForm);

import { useState } from "react";
import api from "../api/axios";

import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { loginSuccess } from "../features/auth/authSlice";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [errors, setErrors] = useState({});
  const dispatch = useDispatch();
  const navigate = useNavigate();

  function validateForm() {
    const newErrors = {};
  
    const usernameRegex = /^[A-Za-z][A-Za-z0-9]{3,19}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex =
      /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]).{6,}$/;
  
    if (!usernameRegex.test(username)) {
      newErrors.username =
        "Логин: 4-20 символов, первая буква, только латиница и цифры";
    }
  
    if (!emailRegex.test(email)) {
      newErrors.email = "Введите корректный email";
    }
  
    if (!passwordRegex.test(password)) {
      newErrors.password =
        "Пароль: минимум 6 символов, заглавная буква, цифра и спецсимвол";
    }
  
    if (password !== password2) {
      newErrors.password2 = "Пароли не совпадают";
    }
  
    setErrors(newErrors);
  
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      await api.post("/api/auth/register/", {
        username,
        full_name: fullName,
        email,
        password,
        password2,
      });
      
      const loginResponse = await api.post("/api/auth/login/", {
        username,
        password,
      });
      
      localStorage.setItem("access", loginResponse.data.access);
      localStorage.setItem("refresh", loginResponse.data.refresh);
      
      dispatch(loginSuccess(loginResponse.data.user));
      
      navigate("/storage");

    } catch (error) {
      console.log("Ошибка регистрации");

      if (error.response) {
        console.log(error.response.data);
      }
    }
  }

  return (
    <div className="page">
      <h1>Регистрация</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <input
            className="inputs"
            type="text"
            placeholder="Логин"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          {errors.username && <p className="err-message">{errors.username}</p>}
        </div>

        <div>
          <input
            className="inputs"
            type="text"
            placeholder="Полное имя"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>

        <div>
          <input
            className="inputs"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          {errors.email && <p className="err-message">{errors.email}</p>}
        </div>

        <div>
          <input
            className="inputs"
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {errors.password && <p className="err-message">{errors.password}</p>}
        </div>

        <div>
          <input
            className="inputs"
            type="password"
            placeholder="Повторите пароль"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
          />
          {errors.password2 && <p className="err-message">{errors.password2}</p>}
        </div>

        <button className="btns" type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
}
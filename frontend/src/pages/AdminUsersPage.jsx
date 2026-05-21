import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import formatFileSize from "../features/formatFileSize";
import formatDate from "../features/formatDate";

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    try {
      const response = await api.get("/api/auth/users/");
      setUsers(response.data.users);
    } catch (error) {
      console.log("Ошибка загрузки пользователей");
    }
  }

  async function deleteUser(userId) {
    if (!window.confirm("Удалить пользователя?")) return;
  
    try {
      await api.delete(`/api/auth/users/${userId}/`);
      loadUsers();
    } catch (error) {
      console.log("Ошибка удаления пользователя");
    }
  }

  async function toggleAdmin(user) {
    try {
      await api.patch(`/api/auth/users/${user.id}/`, {
        is_admin: !user.is_admin,
      });
  
      loadUsers();
    } catch (error) {
      console.log("Ошибка изменения роли");
    }
  }

  function viewFiles(userId) {
    navigate(`/storage?user_id=${userId}`);
  }

  return (
    <div className="page">
      <h1>Админка</h1>

      {users.length === 0 ? (
        <p className="info-msg">Пользователей нет</p>
      ) : (
        <ul className="users-list">
          {users.map((user) => (
            <li className="user" key={user.id}>
              <div className="user-info-container">
                <div className="user-info">{user.username}</div>
                <div className="user-info">{user.is_admin ? "ADMIN" : "USER"}</div>
              </div>
              <div className="user-common-info">
                <span className="user-info-title">ID:
                  <span className="user-info-text"> {user.id}</span>
                </span>
                <span className="user-info-title">Email:
                  <span className="user-info-text"> {user.email}</span>
                </span>
                <span className="user-info-title">Полное имя:
                  <span className="user-info-text"> {user.full_name}</span>
                </span>
                <span className="user-info-title">Дата регистрации:
                  <span className="user-info-text"> {formatDate(user.date_joined)}</span>
                </span>
                <span className="user-info-title">Количество файлов:
                  <span className="user-info-text"> {user.files_count}</span>
                </span>
                <span className="user-info-title">Размер файлов:
                  <span className="user-info-text"> {formatFileSize(user.total_size)}</span>
                </span>
              </div>
              <div className="admin-btns-container">
                <button className="btns admin-btn" onClick={() => toggleAdmin(user)}>
                  Сделать {user.is_admin ? "USER" : "ADMIN"}
                </button>
              
                <button className="btns admin-btn" onClick={() => deleteUser(user.id)}>
                  Удалить
                </button>
              
                <button className="btns admin-btn" onClick={() => viewFiles(user.id)}>
                  Смотреть файлы
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
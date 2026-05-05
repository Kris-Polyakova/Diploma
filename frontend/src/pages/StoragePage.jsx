import { useEffect, useState} from "react";
import api from "../api/axios";
import { useSearchParams } from "react-router-dom";

export default function StoragePage() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [comment, setComment] = useState("");
  const [searchParams] = useSearchParams();
  const userId = searchParams.get("user_id");
  const [viewingUser, setViewingUser] = useState(null);
  const isViewingOtherUser = Boolean(userId);

  useEffect(() => {
    loadFiles();
  }, []);

  async function loadFiles() {
    try {
      const response = await api.get("/api/files/");
      setFiles(response.data);
    } catch (error) {
      console.log("Ошибка загрузки файлов");
    }
  }

  async function uploadFile(e) {
    e.preventDefault();
  
    if (!selectedFile) {
      return;
    }
  
    const formData = new FormData();

    formData.append("file", selectedFile);
    formData.append("original_name", selectedFile.name);
    formData.append("comment", comment);
  
    try {
      await api.post("/api/files/upload/", formData);
  
      setSelectedFile(null);
      setComment("");
  
      loadFiles();
  
    } catch (error) {
      console.log("Ошибка загрузки файла");
    }
  }

  async function deleteFile(fileId) {
    try {
      await api.delete(`/api/files/${fileId}/`);
  
      loadFiles();
  
    } catch (error) {
      console.log("Ошибка удаления файла");
    }
  }

  async function renameFile(file) {
    const newName = prompt(
      "Введите новое имя файла:",
      file.original_name
    );
  
    if (!newName) return;
  
    try {
      await api.patch(`/api/files/${file.id}/`, {
        original_name: newName,
        comment: file.comment || "",
      });
  
      loadFiles();
  
    } catch (error) {
      console.log("Ошибка переименования");
    }
  }

  async function downloadFile(file) {
    try {
      const response = await api.get(`http://127.0.0.1:8000${file.download_url}`, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = url;
      link.download = file.original_name;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Ошибка скачивания:", error);
    }
  }

  async function loadFiles() {
    try {
      const url = userId
        ? `/api/files/?user_id=${userId}`
        : "/api/files/";
  
      const response = await api.get(url);
  
      setFiles(response.data);

      if (userId) {
        setViewingUser(userId);
      } else {
        setViewingUser(null);
      }
  
    } catch (error) {
      console.log("Ошибка загрузки файлов");
    }
  }

  async function copyLink(file) {
    const url = `http://127.0.0.1:8000${file.download_url}`;;
  
    try {
      await navigator.clipboard.writeText(url);
  
      alert("Ссылка скопирована!");
  
    } catch (error) {
      console.log("Ошибка копирования");
    }
  }

  function formatFileName(name) {
    if (name.length <= 20) return name;
  
    const extension = name.split(".").pop();
    const base = name.substring(0, name.lastIndexOf("."));
  
    return base.substring(0, 15) + "..." + extension;
  }

  function isImage(file) {
    return /\.(jpg|jpeg|png|gif|webp)$/i.test(file.original_name);
  }



  return (
    <div className="page">
      <h1>
        {viewingUser
          ? `Файлы пользователя ID: ${viewingUser}`
          : "Моё хранилище"}
      </h1>
      {!isViewingOtherUser && (
        <form onSubmit={uploadFile}>
          <div className="file-input-container">
            <input
              className="inputs file-input"
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />
            <p className="file-input-text">
              {selectedFile
                ? formatFileName(selectedFile.name)
                : "Выбрать файл"}
            </p>
          </div>

          <div>
            <input
              className="inputs"
              type="text"
              placeholder="Комментарий"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </div>

          <button className="btns" type="submit">Загрузить файл</button>
        </form>
      )}

      {files.length === 0 ? (
        <p className="info-msg">Файлов пока нет</p>
      ) : (
        <ul className="files-list">
          {files.map((file) => (
            <li className="file" key={file.id}>
              <div className="prev-container">
                {isImage(file) ? (
                  <img
                    className="prev-image"
                    src={`http://127.0.0.1:8000${file.download_url}`}
                    width={50}
                  />
                ) : (
                  <div className="file-icon">📄</div>
                )}
              </div>
              {file.original_name}
              <div className="file-btns">
                <button className='btns fileBtn' title="Сохранить" onClick={() => downloadFile(file)}>
                  🖫
                </button>

                <button className='btns fileBtn' title="Поделиться ссылкой" onClick={() => copyLink(file)}>
                  ✉
                </button>
              
                <button className='btns fileBtn' title="Переименовать" onClick={() => renameFile(file)}>
                   ✎
                </button>
              
                <button className='btns fileBtn' title="Удалить" onClick={() => deleteFile(file.id)}>
                  ✖
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
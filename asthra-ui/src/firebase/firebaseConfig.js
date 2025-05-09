// src/firebase/firebaseConfig.js
import { initializeApp } from "firebase/app";

const firebaseConfig = {
    apiKey: "AIzaSyButOPX38Vf1OoR074QQZattCUF1vAYgq0",
    authDomain: "asthra-mailguard-77b76.firebaseapp.com",
    projectId: "asthra-mailguard-77b76",
    storageBucket: "asthra-mailguard-77b76.firebasestorage.app",
    messagingSenderId: "991829562063",
    appId: "1:991829562063:web:6250734c6c85b20a505dba",
    measurementId: "G-NQ34YK3D12"
  
};

export const firebaseApp = initializeApp(firebaseConfig);

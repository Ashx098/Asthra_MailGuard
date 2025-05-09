// src/firebase/auth.js
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
import { firebaseApp } from "./firebaseConfig";

export const auth = getAuth(firebaseApp);
export const provider = new GoogleAuthProvider();

export const signInWithGoogle = () => signInWithPopup(auth, provider);
export const logout = () => signOut(auth);

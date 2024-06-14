import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Login from './components/Login.jsx';
import InputToken from './components/InputToken.jsx';
import Profile from './components/Profile.jsx';
import Stations from "./components/Stations.jsx";
import Reservations from './components/Reservations.jsx';
import NotFound from './components/NotFound.jsx';
const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login/>}/>
                <Route path="/token" element={<InputToken/>}/>
                <Route path="/me" element={<Profile/>}/>
                <Route path="/reservations" element={<Reservations/>}/>
                <Route path="/stations" element={<Stations/>}/>

                <Route path="*" element={<NotFound/>}/>
            </Routes>
        </Router>
    );
};

export default AppRouter;
import React from 'react';
import AppRouter from './AppRouter';


const App = () => {


    return (
        <div style={styles.container}>
            <AppRouter/>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: 'white',
    },
};

export default App;

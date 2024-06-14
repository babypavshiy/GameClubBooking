import React, {useState} from 'react';
import {Button, Form, Input, message} from 'antd';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import UrlAddr from "../../Url/UrlAddr.js";

const Login = () => {
    const [loading, setLoading] = useState(false);
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();


    const onFinish = async (values) => {
    setLoading(true);
    const { email, password, username } = values;

    const endpoint = isLogin ? '/users/login' : '/users/register';
    const data = isLogin
        ? new URLSearchParams({
            grant_type: '',
            username: email,
            password: password,
            scope: '',
            client_id: '',
            client_secret: '',
        })
        : {
            email: email,
            password: password,
            is_active: true,
            is_superuser: false,
            is_verified: false,
            username: username,
            role_id: 0
        };

    try {
        const response = await axios.post(UrlAddr + `${endpoint}`, data, {
            headers: {
                'accept': 'application/json',
                'Content-Type': isLogin ? 'application/x-www-form-urlencoded' : 'application/json',
            },
            withCredentials: true
        });

        console.log(response.data);

        if (!isLogin) {
                await axios.post(UrlAddr + '/users/request-verify-token', {
                    email,
                }, {
                    headers: {
                        'accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                });
                navigate("/token")
            }


        if (isLogin)
                navigate("/reservations");
            message.success(isLogin ? 'Вы вошли в систему' : 'ВЫ зарегистрированы! Проверьте почту');
            console.log('Response:', response.data);

    } catch (error) {
        message.error(isLogin ? 'Неудачный вход' : 'Регистрация завершилась неудачно');
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
};


    return (
        <div style={styles.formContainer}>
            <div style={styles.tabButtons}>
                <Button type={isLogin ? 'primary' : 'default'} onClick={() => setIsLogin(true)}>Войти</Button>
                <Button type={!isLogin ? 'primary' : 'default'}
                        onClick={() => setIsLogin(false)}>Зарегистрироваться</Button>
            </div>

            <Form
                name={isLogin ? "Войти" : "Зарегистрироваться"}
                initialValues={{remember: true}}
                onFinish={onFinish}
                layout="vertical"
                style={styles.form}
            >
                <Form.Item
                    label="Email"
                    name="email"
                    rules={[{required: true, message: 'Пожалуйста, введите ваш email!'}]}
                >
                    <Input/>
                </Form.Item>

                {!isLogin && (
                    <Form.Item
                        label="Юзернейм"
                        name="username"
                        rules={[{required: true, message: 'Пожалуйста, введите ваш юзернейм!'}]}
                    >
                        <Input/>
                    </Form.Item>
                )}

                <Form.Item
                    label="Пароль"
                    name="password"
                    rules={[{required: true, message: 'Пожалуйста, введите пароль!'}]}
                >
                    <Input.Password/>
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} style={styles.button}>
                        {isLogin ? 'Войти' : 'Зарегистрироваться'}
                    </Button>
                </Form.Item>
            </Form>
        </div>

    );
};

const styles = {
    formContainer: {
        width: '100%',
        maxWidth: 400,
        padding: '20px',
        backgroundColor: 'white',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    },
    form: {
        width: '100%',
    },
    button: {
        width: '100%',
        marginTop: '10px',
    },
    tabButtons: {
        marginBottom: '20px',
    }
};

export default Login;

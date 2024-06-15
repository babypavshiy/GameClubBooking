import React, {useState} from 'react';
import {Button, Form, Input, message} from 'antd';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import UrlAddr from "../../Url/UrlAddr.js";

const InputToken = () => {
    const navigate = useNavigate();

    const onFinish = async (values) => {
        const {token} = values;

        try {
            const response = await axios.post(UrlAddr + '/users/verify', {token}, {
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            });

            message.success('Token verification successful');
            console.log('Response:', response.data);
            navigate('/');
        } catch (error) {
            message.error('Token verification failed');
            console.error('Error:', error);
        }
    };

    return (
        <div style={styles.container}>
            <Form
                name="input-token"
                onFinish={onFinish}
                layout="vertical"
            >
                <Form.Item
                    label="Token"
                    name="token"
                    rules={[{required: true, message: 'Please input your token!'}]}
                >
                    <Input/>
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit">
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

const styles = {
    container: {
        width: '100%',
        maxWidth: 400,
        margin: '20px auto',
        padding: '20px',
        backgroundColor: 'white',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    },
};

export default InputToken;

import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {Button, Descriptions, Form, Input, Layout, Menu, message, Modal, Spin, theme} from 'antd';
import {HomeOutlined, LogoutOutlined, UserOutlined, LaptopOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";
import UrlAddr from "../../Url/UrlAddr.js";


const {Content, Footer, Sider} = Layout;

const Profile = () => {
    const [user, setUser] = useState(null);
    const [collapsed, setCollapsed] = useState(false);
    const [loading, setLoading] = useState(true);
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [form] = Form.useForm();
    const navigate = useNavigate();

    const {
        token: {borderRadiusLG},
    } = theme.useToken();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get(UrlAddr + '/users/me', {
                    headers: {
                        "accept": "application/json",
                    },
                    withCredentials: true,
                });
                setUser(response.data);
            } catch (error) {
                message.error('Failed to fetch user information');
                console.error('Error:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, []);

    const handleLogout = async () => {
        try {
            await axios.post(UrlAddr + '/users/logout', {}, {withCredentials: true});
            message.success('Вы успешно вышли из системы');
            navigate('/');
        } catch (error) {
            message.error('Не удалось выполнить выход из системы');
            console.error('Error:', error);
        }
    };

    const showEditModal = () => {
        form.setFieldsValue({username: user.username});
        setEditModalVisible(true);
    };

    const handleEditProfile = async (values) => {
        try {
            await axios.patch(
                UrlAddr + '/users/me',
                {
                    password: values.password,
                    email: user.email,
                    is_active: user.is_active,
                    is_superuser: user.is_superuser,
                    is_verified: user.is_verified,
                    username: values.username,
                    games_played: user.games_played,
                    games_organized: user.games_organized,
                    role_id: user.role_id,
                },
                {
                    headers: {
                        "accept": "application/json",
                    },
                    withCredentials: true,
                }
            );
            message.success('Profile updated successfully');
            setEditModalVisible(false);
            const response = await axios.get(UrlAddr + '/users/me/', {
                headers: {
                    "accept": "application/json",
                },
                withCredentials: true,
            });
            setUser(response.data);
        } catch (error) {
            message.error('Failed to update profile');
            console.error('Error:', error);
        }
    };

    if (loading) {
        return <Spin size="large"/>;
    }


    return (
        <Layout
            style={{
                minHeight: '100vh',
            }}
        >
            <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}
            >
                <div className="demo-logo-vertical"/>
                <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
                    <Menu.Item key="reservations" icon={<HomeOutlined/>}>
                        <Link to="/reservations">Мои записи</Link>
                    </Menu.Item>
                    <Menu.Item key="profile" icon={<UserOutlined/>}>
                        <Link to="/me">Мой профиль</Link>
                    </Menu.Item>
                    <Menu.Item key="stations" icon={<LaptopOutlined />}>
                        <Link to="/stations">Устройства</Link>
                    </Menu.Item>
                    <Menu.Item key="logout" icon={<LogoutOutlined/>} onClick={handleLogout}>
                        Выход
                    </Menu.Item>
                </Menu>

            </Sider>

            <Layout>
                <Content
                    style={{
                        margin: '0 16px',
                        padding: 24,
                        minHeight: 360,
                        borderRadius: borderRadiusLG,
                        marginTop: 20
                    }}
                >
                    <h1 style={{
                        textAlign: 'center',
                        fontSize: 32,
                        marginBottom: 16,
                    }}>
                        Мой профиль
                    </h1>

                    <Descriptions title="Информация" bordered>
                        <Descriptions.Item label="Юзернейм">{user.username}</Descriptions.Item>
                        <Descriptions.Item label="Email">{user.email}</Descriptions.Item>
                        <Descriptions.Item label="ID">{user.id}</Descriptions.Item>
                    </Descriptions>

                    <Button type="primary" onClick={showEditModal} style={{marginTop: 16}}>
                        Изменить профиль
                    </Button>

                    <Modal
                        title="Изменить профиль"
                        visible={editModalVisible}
                        onCancel={() => setEditModalVisible(false)}
                        onOk={() => form.submit()}
                    >
                        <Form form={form} onFinish={handleEditProfile}>
                            <Form.Item
                                name="username"
                                label="Username"
                                rules={[{required: true, message: 'Please input your username!'}]}
                            >
                                <Input/>
                            </Form.Item>
                            <Form.Item
                                name="password"
                                label="Password"
                                rules={[{required: true, message: 'Please input your password!'}]}
                            >
                                <Input.Password/>
                            </Form.Item>
                        </Form>
                    </Modal>

                </Content>
                <Footer
                    style={{
                        textAlign: 'center',
                    }}
                >
                    GameClubBooking ©{new Date().getFullYear()} Created by babypavshiy
                </Footer>
            </Layout>
        </Layout>
    );
};

export default Profile;

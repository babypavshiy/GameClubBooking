import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {Card, Spin, Row, Col, message, Menu, Layout, Descriptions, Button, Modal, Form, Input, theme, List, Rate} from 'antd';
import {HomeOutlined, LaptopOutlined, LogoutOutlined, UserOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";
import UrlAddr from "../../Url/UrlAddr.js";

const {Content, Footer, Sider} = Layout;

function formatDate(isoString) {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);

    return `${day}.${month}.${year}`;
}

function formatTime(isoString) {
    const date = new Date(isoString);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${hours}:${minutes}`;
}


const Stations = () => {
    const [stations, setStations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [collapsed, setCollapsed] = useState(false);
        const [reviewsModalVisible, setReviewsModalVisible] = useState(false);
    const [selectedStationReviews, setSelectedStationReviews] = useState([]);
    const [selectedStationName, setSelectedStationName] = useState('');
    const [addReviewModalVisible, setAddReviewModalVisible] = useState(false);
    const [selectedStationId, setSelectedStationId] = useState(null);
    const [rating, setRating] = useState(5);
    const navigate = useNavigate();

const {
        token: {borderRadiusLG},
    } = theme.useToken();
    useEffect(() => {
        const fetchStations = async () => {
            try {
                const response = await axios.get(UrlAddr + '/stations/', {withCredentials: true});
                setStations(response.data);
            } catch (error) {
                message.error('Failed to fetch stations');
            } finally {
                setLoading(false);
            }
        };

        fetchStations();
    }, []);

    if (loading) {
        return <Spin size="large" style={{ display: 'block', margin: 'auto' }} />;
    }

    const handleLogout = async () => {
        try {
            await axios.post(UrlAddr + '/users/logout/', {}, {withCredentials: true});
            message.success('Вы успешно вышли из системы');
            navigate('/');
        } catch (error) {
            message.error('Не удалось выполнить выход из системы');
            console.error('Error:', error);
        }
    };

    const handleViewReviews = async (stationId, stationName) => {
        try {
            const response = await axios.get(UrlAddr + `/reviews/by_station/${stationId}`, {withCredentials: true});
            setSelectedStationReviews(response.data.data);
            setSelectedStationId(stationId);
            setSelectedStationName(stationName);
            setReviewsModalVisible(true);
        } catch (error) {
            message.error('Failed to fetch reviews');
        }
    };

    const handleAddReview = (stationId, stationName) => {
        setSelectedStationId(stationId);
        console.log(stationId, selectedStationId)
        setSelectedStationName(stationName);
        setAddReviewModalVisible(true);
    };

    const handleAddReviewSubmit = async (values) => {
        try {
            console.log(selectedStationId)
            const { comment } = values;
            const data = {
                station_id: selectedStationId,
                rating,
                comment,
            };

            await axios.post(UrlAddr + '/reviews/', data, {withCredentials: true});
            message.success('Review added successfully');
            setAddReviewModalVisible(false);
        } catch (error) {
            message.error('Failed to add review');
        }
    };

    const handleCloseReviewsModal = () => {
        setReviewsModalVisible(false);
        setSelectedStationId(null);
        setSelectedStationName('');
        setSelectedStationReviews([]);
    };

    const handleCloseAddReviewModal = () => {
        setAddReviewModalVisible(false);
    };

    const handleRatingChange = (value) => {
        setRating(value);
    };


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
                    <Row gutter={[16, 16]}>
            {stations.map(station => (
                <Col span={8} key={station.id}>
                    <Card title={station.name}>
                        <p><strong>Номер устройства: </strong> {station.id}</p>
                        <p><strong>Тип устройства: </strong> {station.type}</p>
                        <Button type="primary" onClick={() => handleViewReviews(station.id, station.name)}>Посмотреть отзывы</Button>
                        <Button onClick={() => handleAddReview(station.id, station.name)} style={{ marginLeft: 8 }}>Добавить отзыв</Button>
                    </Card>
                </Col>
            ))}
        </Row>

                    <Modal
                title={`Reviews for ${selectedStationName}`}
                open={reviewsModalVisible}
                onCancel={handleCloseReviewsModal}
                footer={null}
            >
                <List
                    dataSource={selectedStationReviews}
                    renderItem={review => (
                        <List.Item>
                            <Card>
                                <p><strong>От пользователя:</strong> {review.user_id}</p>
                                <p><strong>Оценка:</strong> {review.rating}</p>
                                <p><strong>Комментарий:</strong> {review.comment}</p>
                                <p><strong>Оставлен:</strong> {formatDate(review.created_at)} {formatTime(review.created_at)}</p>
                            </Card>
                        </List.Item>
                    )}
                />
                    </Modal>

                <Modal
                title={`Add Review for ${selectedStationName}`}
                visible={addReviewModalVisible}
                onCancel={handleCloseAddReviewModal}
                footer={null}
            >
                <Form layout="vertical" onFinish={handleAddReviewSubmit}>
                    <Form.Item name="rating" label="Rating">
                        <Rate allowHalf value={rating} onChange={handleRatingChange} />
                    </Form.Item>
                    <Form.Item name="comment" label="Comment" rules={[{ required: true, message: 'Please input your comment' }]}>
                        <Input rows={4} />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Добавить
                        </Button>
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

export default Stations;

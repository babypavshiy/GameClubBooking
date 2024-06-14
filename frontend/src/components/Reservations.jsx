import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Card,
    Row,
    Col,
    Spin,
    message,
    Button,
    Modal,
    Form,
    Input,
    Select,
    DatePicker,
    TimePicker,
    Layout,
    theme, Menu
} from 'antd';
import dayjs from 'dayjs';
import {HomeOutlined, LaptopOutlined, LogoutOutlined, UserOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";
import UrlAddr from "../../Url/UrlAddr.js";



const {Content, Footer, Sider} = Layout;

const { Meta } = Card;
const { Option } = Select;
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


const Reservations = () => {
    const [collapsed, setCollapsed] = useState(false);
const [reservations, setReservations] = useState([]);
    const [stations, setStations] = useState([]);
    const [stationsMap, setStationsMap] = useState({});
    const [loading, setLoading] = useState(true);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const navigate = useNavigate();

    const {
        token: {borderRadiusLG},
    } = theme.useToken();

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

    useEffect(() => {
        const fetchReservations = async () => {
            try {
                const [reservationsResponse, stationsResponse] = await Promise.all([
                    axios.get(UrlAddr + '/reservations/', {withCredentials: true}),
                    axios.get(UrlAddr + '/stations/', {withCredentials: true}),
                ]);

                const reservationsData = reservationsResponse.data.data;
                const stationsData = stationsResponse.data;
                console.log(stationsData);
                setReservations(reservationsData);
                setStations(stationsData);

                const stationsMapData = {};
                stationsData.forEach(station => {
                    stationsMapData[station.id] = station;
                });

                setStationsMap(stationsMapData);
            } catch (error) {
                message.error('Failed to fetch reservations or stations');
            } finally {
                setLoading(false);
            }
        };

        fetchReservations();
    }, []);

    if (loading) {
        return <Spin size="large" style={{ display: 'block', margin: 'auto' }} />;
    }

    const showModal = () => {
        setIsModalVisible(true);
    };

    const showModalPay = (data) => {

        console.log(data.payment_url);
        Modal.success({
            title: 'Результат запроса',
            content: (
                <div>
                    <p>Игра успешно добавлена!</p>
                    <Button type="primary" href={data.payment_url} target="_blank" rel="noopener noreferrer">
                        Оплатить
                    </Button>
                </div>
            ),
            onOk() {
                console.log('Ок');
            },
        });
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const handleCreate = async (values) => {
        try {
            const { station_id, status, amount, date, start_time } = values;
            const formattedDate = dayjs(date).format('YYYY-MM-DD');
            const formattedStartTime = dayjs(start_time).format('YYYY-MM-DDTHH:mm:ss');

            const data = {
                station_id,
                status: 0,
                amount,
                date: formattedDate,
                start_time: formattedStartTime,
            };

            const add_response = await axios.post(UrlAddr + '/reservations/', data, {
                headers: {
                    'Content-Type': 'application/json',
                },
                withCredentials: true
            });

            showModalPay(add_response.data.data);

            message.success('Reservation created successfully');
            setIsModalVisible(false);

            // Fetch updated reservations list
            const response = await axios.get(UrlAddr + '/reservations/', {withCredentials: true});
            setReservations(response.data.data);
        } catch (error) {
            message.error('Failed to create reservation');
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(UrlAddr + `/reservations/${id}`, {withCredentials: true});
            message.success('Reservation deleted successfully');

            const response = await axios.get(UrlAddr + '/reservations/', {withCredentials: true});
            setReservations(response.data.data);
        } catch (error) {
            message.error('Failed to delete reservation');
        }
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

                    <Button type="primary" onClick={showModal} style={{ marginBottom: 16 }}>
                Записаться
            </Button>

                    <Row gutter={[16, 16]}>
            {reservations.map((reservation) => {
             const station = stationsMap[reservation.station_id];
            return  (  <Col span={8} key={reservation.id}>
                    <Card
                        hoverable
                        title={formatDate(reservation.date)}
                        actions={[
                                    <Button type="primary" danger onClick={() => handleDelete(reservation.id)}>Отписаться</Button>
                                ]}
                    >
                        <p>
                            <b>Время начала: </b> {formatTime(reservation.start_time)}
                        </p>
                        <p>
                            <b>Время конца: </b> {formatTime(reservation.end_time)}
                        </p>
                        <p>
                            <b>Номер устройства: </b> {reservation.station_id}
                        </p>
                        {station &&
                            <div>
                            <p><strong>Имя устройства: </strong> {station.name}</p>
                            <p><strong>Тип устройства:</strong> {station.type}</p>
                        </div>}
                    </Card>
            </Col>)

                }
            )}
                    </Row>

                    <Modal title="Создать новую запись" open={isModalVisible} onCancel={handleCancel} footer={null}>
                <Form layout="vertical" onFinish={handleCreate}>
                    <Form.Item name="station_id" label="Устройство" rules={[{ required: true, message: 'Пожалуйста, выберите устройство' }]}>
                        <Select placeholder="ВЫберите устрйоство">
                            {stations.map((station) => (
                                <Option key={station.id} value={station.id}>
                                    {station.name}
                                </Option>
                            ))}
                        </Select>
                    </Form.Item>
                    <Form.Item name="date" label="Дата" rules={[{ required: true, message: 'Пожалуйста, выберите дату'  }]}>
                        <DatePicker />
                    </Form.Item>
                    <Form.Item name="start_time" label="Время начала" rules={[{ required: true, message: 'Пожалуйста, выберите время начала'  }]}>
                        <TimePicker />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="Записаться">
                            Create
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

export default Reservations;

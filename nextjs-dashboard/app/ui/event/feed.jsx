"use client"
import Button from '@mui/material/Button';

export default function Feed() {
    const handleRouteChange = (url) => {
        window.location.href = url;
    }

    return (
        <div>
            <Button variant="contained" color="primary"
                    onClick={() => handleRouteChange('http://127.0.0.1:5000/mood_feed')}>
                情感检测
            </Button>
            <Button variant="contained" color="primary"
                    onClick={() => handleRouteChange('http://127.0.0.1:5000/pose_feed')}>
                跌倒检测
            </Button>
            <Button variant="contained" color="primary"
                    onClick={() => handleRouteChange('http://127.0.0.1:5000/face_feed')}>
                人脸检测
            </Button>
            <Button variant="contained" color="primary"
                    onClick={() => handleRouteChange('http://127.0.0.1:5000/object_feed')}>
                物品检测
            </Button>
        </div>
    )
}
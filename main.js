const express = require('express');
const cors = require('cors');
const emoji = require('emoji-js');

const app = express();

const emojiPicker = new emoji.EmojiConvertor();

app.use(cors());

app.get('/api/random-emoji', (req, res) => {
    const length = req.query.length || '1';
    
    try {
        const num = parseFloat(length);
        if (Number.isInteger(num) && num > 0) {
            const emojis = Object.keys(emojiPicker.EMOJI_MAP);
            const randomEmojis = Array.from({ length: num }, () => emojis[Math.floor(Math.random() * emojis.length)]).join('');
            return res.json({
                success: true,
                result: randomEmojis
            });
        } else {
            throw new Error('Invalid length');
        }
    } catch (error) {
        return res.status(400).json({
            success: false,
            message: 'Length must be a positive integer.'
        });
    }
});

app.get('/api/random-string', (req, res) => {
    const length = req.query.length || '1';

    try {
        const num = parseFloat(length);
        if (Number.isInteger(num) && num > 0) {
            const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            const randomString = Array.from({ length: num }, () => characters[Math.floor(Math.random() * characters.length)]).join('');
            return res.json({
                success: true,
                result: randomString
            });
        } else {
            throw new Error('Invalid length');
        }
    } catch (error) {
        return res.status(400).json({
            success: false,
            message: 'Length must be a positive integer.'
        });
    }
});

app.listen(3000);

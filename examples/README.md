# 📁 Examples - BrJoy WebP Optimizer

Example files to help you understand the tool's output.

## Files

### `AI-CODE-UPDATE-EXAMPLE.txt`
Example of the AI-friendly report generated after conversion.

**Use this to:**
- Understand the report format
- Test with AI assistants
- See what to expect after conversion

**How to use:**
1. Copy the content
2. Send to Claude/ChatGPT/Copilot
3. Add prompt: "Update all image URLs from this report in my code"
4. AI will find and replace all references

---

## Real-World Example

### Before Conversion
Your project has these images:
```
src/
  images/
    hero.png (2.4 MB)
    blog-post.jpg (1.7 MB)
    thumbnail.png (439 KB)
```

### After Conversion
BrJoy creates:
```
output/
  hero.webp (830 KB) - 66% smaller
  blog-post.webp (703 KB) - 60% smaller
  thumbnail.webp (176 KB) - 60% smaller
  
  conversion-report.html - Visual report
  AI-CODE-UPDATE.txt - For AI
  conversions.csv - For spreadsheets
```

### AI Updates Your Code
Send `AI-CODE-UPDATE.txt` to AI, and it updates:

**HTML:**
```html
<!-- Before -->
<img src="images/hero.png" alt="Hero">

<!-- After -->
<img src="images/hero.webp" alt="Hero">
```

**CSS:**
```css
/* Before */
.banner {
  background-image: url('images/hero.png');
}

/* After */
.banner {
  background-image: url('images/hero.webp');
}
```

**React:**
```jsx
// Before
import hero from './images/hero.png';

// After
import hero from './images/hero.webp';
```

---

## Tips

1. **Always backup** your code before AI updates
2. **Review changes** after AI completes
3. **Test thoroughly** to ensure all paths work
4. **Use version control** (git) for safety

---

## Need Help?

- 📖 Read: [QUICKSTART.md](../QUICKSTART.md)
- 🐛 Report: [GitHub Issues](https://github.com/ibrumatte/brjoy-webp-optimizer/issues)
- 💬 Discuss: [GitHub Discussions](https://github.com/ibrumatte/brjoy-webp-optimizer/discussions)

const fs = require("fs");
const path = require("path");
const sharp = require("sharp");

const settings = {
  inDirectoryName: "images",
  outDirectoryName: "compressed",
	format: "webp",
	quality: 100,
	width: 1920,
	height: 1080,
	fit: "cover", // https://sharp.pixelplumbing.com/api-resize#resize
	background: { r: 255, g: 255, b: 255, alpha: 1 }, // when fit is cover or contain
	withoutEnlargement: true,
};

const images = fs.readdirSync(path.join(__dirname, settings.inDirectoryName));

images.forEach(async (image) => {
	const originalFileSize =
		fs.statSync(path.join(__dirname, settings.inDirectoryName, image)).size /
		(1024 * 1024);

	const imageBuffer = await sharp(
		path.join(__dirname, settings.inDirectoryName, image)
	).toBuffer();

	console.log(
		`Converting ${image} with a file size of ${originalFileSize.toFixed(
			2
		)} MB to ${settings.format}`
	);

	const transformedImg = sharp(imageBuffer)
		.toFormat(settings.format, { quality: settings.quality })
		.resize(settings.width, settings.height, {
			fit: settings.fit,
			background: settings.background,
			withoutEnlargement: settings.withoutEnlargement,
    });

  await transformedImg.toFile(path.join(__dirname, settings.outDirectoryName, `${image.split(".")[0]}.${settings.format}`));

  const newFileSize = fs.statSync(path.join(__dirname, settings.outDirectoryName, `${image.split(".")[0]}.${settings.format}`)).size / (1024 * 1024);

  console.log(`${image.split(".")[0]}.${settings.format} new file size is ${newFileSize.toFixed(2)} MB`);
});

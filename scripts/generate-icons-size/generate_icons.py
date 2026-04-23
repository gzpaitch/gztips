#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SUPPORTED_INPUTS = {".png", ".svg"}
SUPPORTED_FORMATS = {"png", "webp", "ico"}
DEFAULT_SIZES = [16, 32, 48, 96, 128, 192]
DEFAULT_FORMATS = ["png"]
IGNORED_DIRS = {".git", ".venv", "node_modules", "__pycache__"}


def parse_csv(value: str) -> list[str]:
	return [item.strip() for item in value.split(",") if item.strip()]


def parse_sizes(value: str) -> list[int]:
	sizes: list[int] = []

	for raw_size in parse_csv(value):
		if not raw_size.isdigit():
			raise ValueError(f"Invalid size: {raw_size}")

		size = int(raw_size)
		if size <= 0:
			raise ValueError(f"Size must be greater than zero: {raw_size}")

		sizes.append(size)

	if not sizes:
		raise ValueError("At least one size is required.")

	return sorted(set(sizes))


def parse_formats(value: str) -> list[str]:
	formats = [item.lower().lstrip(".") for item in parse_csv(value)]
	invalid_formats = sorted(set(formats) - SUPPORTED_FORMATS)

	if invalid_formats:
		supported = ", ".join(sorted(SUPPORTED_FORMATS))
		raise ValueError(f"Unsupported format(s): {', '.join(invalid_formats)}. Supported: {supported}")

	if not formats:
		raise ValueError("At least one format is required.")

	return sorted(set(formats))


def is_ignored(path: Path) -> bool:
	return any(part in IGNORED_DIRS for part in path.parts)


def find_sources(root: Path) -> list[Path]:
	return sorted(
		path
		for path in root.rglob("*")
		if path.is_file()
		and path.suffix.lower() in SUPPORTED_INPUTS
		and not is_ignored(path.relative_to(root))
	)


def ask_source(root: Path, source_arg: str | None) -> Path:
	if source_arg:
		source = Path(source_arg).expanduser()
		if not source.is_absolute():
			source = root / source

		return validate_source(source)

	sources = find_sources(root)
	if not sources:
		raise ValueError(f"No .svg or .png files found under {root}")

	print("Source images found:")
	for index, source in enumerate(sources, start=1):
		print(f"  {index}. {source.relative_to(root)}")

	while True:
		answer = input(f"Choose the source image [1-{len(sources)}]: ").strip()
		if answer.isdigit() and 1 <= int(answer) <= len(sources):
			return validate_source(sources[int(answer) - 1])

		print("Invalid choice. Enter one of the listed numbers.")


def ask_sizes(sizes_arg: str | None) -> list[int]:
	if sizes_arg:
		return parse_sizes(sizes_arg)

	default_value = ",".join(str(size) for size in DEFAULT_SIZES)
	answer = input(f"Output sizes in px, comma-separated [{default_value}]: ").strip()
	return parse_sizes(answer or default_value)


def ask_formats(formats_arg: str | None) -> list[str]:
	if formats_arg:
		return parse_formats(formats_arg)

	default_value = ",".join(DEFAULT_FORMATS)
	answer = input(f"Output formats ({', '.join(sorted(SUPPORTED_FORMATS))}) [{default_value}]: ").strip()
	return parse_formats(answer or default_value)


def ask_output_dir(root: Path, output_arg: str | None, source: Path) -> Path:
	if output_arg:
		output_dir = Path(output_arg).expanduser()
		return output_dir if output_dir.is_absolute() else root / output_dir

	slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", source.stem).strip("-").lower() or "icons"
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
	default_output = Path("generated-icons") / f"{slug}-{timestamp}"
	answer = input(f"Output folder [{default_output}]: ").strip()
	output_dir = Path(answer) if answer else default_output
	return output_dir if output_dir.is_absolute() else root / output_dir


def build_default_output_dir(root: Path, source: Path) -> Path:
	slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", source.stem).strip("-").lower() or "icons"
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
	return root / "generated-icons" / f"{slug}-{timestamp}"


def validate_source(source: Path) -> Path:
	source = source.resolve()

	if not source.exists() or not source.is_file():
		raise ValueError(f"Source file does not exist: {source}")

	if source.suffix.lower() not in SUPPORTED_INPUTS:
		raise ValueError("Source must be a .svg or .png file.")

	return source


def load_pillow():
	try:
		from PIL import Image
	except ImportError as error:
		raise RuntimeError("Missing dependency: Pillow. Install it with: python -m pip install pillow") from error

	return Image


def render_svg(source: Path, size: int) -> bytes:
	try:
		import cairosvg
	except ImportError as error:
		raise RuntimeError("Missing dependency for SVG input: cairosvg. Install it with: python -m pip install cairosvg") from error

	return cairosvg.svg2png(url=str(source), output_width=size, output_height=size)


def load_image(source: Path, size: int):
	Image = load_pillow()

	if source.suffix.lower() == ".svg":
		return Image.open(io.BytesIO(render_svg(source, size))).convert("RGBA")

	return Image.open(source).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)


def save_icon(source: Path, output_dir: Path, size: int, file_format: str) -> Path:
	image = load_image(source, size)
	output_path = output_dir / f"icon{size}.{file_format}"

	if file_format == "ico":
		image.save(output_path, format="ICO", sizes=[(size, size)])
	else:
		image.save(output_path, format=file_format.upper())

	return output_path


def copy_source(source: Path, output_dir: Path) -> Path:
	output_path = output_dir / source.name
	shutil.copy2(source, output_path)
	return output_path


def create_icons(source: Path, sizes: list[int], formats: list[str], output_dir: Path, copy_original: bool) -> list[Path]:
	output_dir.mkdir(parents=True, exist_ok=False)

	created_files: list[Path] = []
	if copy_original:
		created_files.append(copy_source(source, output_dir))

	for size in sizes:
		for file_format in formats:
			created_files.append(save_icon(source, output_dir, size, file_format))

	return created_files


def run_gui(root: Path) -> int:
	try:
		import tkinter as tk
		from tkinter import filedialog, messagebox, ttk
	except ImportError as error:
		print("Error: tkinter is not available. Run with --cli to use the terminal wizard.", file=sys.stderr)
		return 1

	window = tk.Tk()
	window.title("Icon Forge")
	window.geometry("900x660")
	window.minsize(820, 600)
	window.configure(bg="#f4f1ea")

	style = ttk.Style(window)
	style.theme_use("clam")
	style.configure(".", font=("Segoe UI", 10), background="#f4f1ea", foreground="#1f2933")
	style.configure("App.TFrame", background="#f4f1ea")
	style.configure("Hero.TFrame", background="#17211f")
	style.configure("Card.TFrame", background="#fffaf0", relief="flat")
	style.configure("Panel.TLabelframe", background="#fffaf0", bordercolor="#d9c9ad", relief="solid")
	style.configure("Panel.TLabelframe.Label", background="#fffaf0", foreground="#5f3f12", font=("Segoe UI", 10, "bold"))
	style.configure("TLabel", background="#f4f1ea", foreground="#1f2933")
	style.configure("HeroTitle.TLabel", background="#17211f", foreground="#fff7e6", font=("Segoe UI", 22, "bold"))
	style.configure("HeroSub.TLabel", background="#17211f", foreground="#d7c7a4", font=("Segoe UI", 10))
	style.configure("CardTitle.TLabel", background="#fffaf0", foreground="#17211f", font=("Segoe UI", 12, "bold"))
	style.configure("Muted.TLabel", background="#fffaf0", foreground="#74695a", font=("Segoe UI", 9))
	style.configure("Summary.TLabel", background="#fffaf0", foreground="#1f2933", font=("Consolas", 9))
	style.configure("Status.TLabel", background="#f4f1ea", foreground="#5f3f12", font=("Segoe UI", 9))
	style.configure("TEntry", fieldbackground="#fffdf7", bordercolor="#d9c9ad", lightcolor="#d9c9ad", darkcolor="#d9c9ad")
	style.configure("TCheckbutton", background="#fffaf0", foreground="#1f2933")
	style.map("TCheckbutton", background=[("active", "#fffaf0")])
	style.configure("TButton", background="#eadcc2", foreground="#17211f", borderwidth=0, focusthickness=0, padding=(12, 8))
	style.map("TButton", background=[("active", "#dcc8a5"), ("pressed", "#cdb58d")])
	style.configure("Primary.TButton", background="#d96f32", foreground="#fffaf0", font=("Segoe UI", 10, "bold"), padding=(18, 10))
	style.map("Primary.TButton", background=[("active", "#bf5f2a"), ("pressed", "#a94f21")])
	style.configure("Preset.TButton", background="#fff2d2", foreground="#5f3f12", padding=(10, 7))
	style.map("Preset.TButton", background=[("active", "#f2dfb5"), ("pressed", "#e7cd9e")])
	style.configure("Horizontal.TProgressbar", background="#d96f32", troughcolor="#eadcc2", bordercolor="#eadcc2", lightcolor="#d96f32", darkcolor="#d96f32")

	source_var = tk.StringVar()
	output_var = tk.StringVar()
	custom_sizes_var = tk.StringVar()
	copy_source_var = tk.BooleanVar(value=True)
	status_var = tk.StringVar(value="Choose a source image to start.")
	summary_var = tk.StringVar(value="No source selected yet.")
	size_vars = {size: tk.BooleanVar(value=size in {16, 48, 128, 192}) for size in DEFAULT_SIZES}
	format_vars = {file_format: tk.BooleanVar(value=file_format == "png") for file_format in sorted(SUPPORTED_FORMATS)}
	presets = {
		"Chrome": [16, 48, 128],
		"PWA": [48, 96, 128, 192],
		"Favicons": [16, 32, 48],
		"All": DEFAULT_SIZES,
	}

	def current_source() -> Path | None:
		if not source_var.get().strip():
			return None

		return Path(source_var.get()).expanduser()

	def suggest_output_dir(source: Path) -> None:
		output_var.set(str(build_default_output_dir(root, source)))

	def relative_text(path_text: str) -> str:
		if not path_text:
			return "Not selected"

		path = Path(path_text).expanduser()
		try:
			return str(path.resolve().relative_to(root))
		except (OSError, ValueError):
			return str(path)

	def browse_source() -> None:
		filename = filedialog.askopenfilename(
			title="Choose source image",
			filetypes=[("Images", "*.png *.svg"), ("PNG", "*.png"), ("SVG", "*.svg")],
			initialdir=root,
		)
		if not filename:
			return

		source = Path(filename)
		source_var.set(str(source))
		suggest_output_dir(source)
		status_var.set(f"Ready to generate icons from {source.name}.")
		update_summary()

	def browse_output() -> None:
		initialdir = Path(output_var.get()).parent if output_var.get().strip() else root / "generated-icons"
		folder = filedialog.askdirectory(title="Choose parent folder", initialdir=initialdir)
		if not folder:
			return

		source = current_source()
		folder_path = Path(folder)
		if source:
			output_var.set(str(folder_path / build_default_output_dir(root, source).name))
		else:
			output_var.set(str(folder_path / "generated-icons"))
		update_summary()

	def selected_sizes() -> list[int]:
		values = [size for size, enabled in size_vars.items() if enabled.get()]
		custom_value = custom_sizes_var.get().strip()
		if custom_value:
			values.extend(parse_sizes(custom_value))

		if not values:
			raise ValueError("Choose at least one size.")

		return sorted(set(values))

	def selected_formats() -> list[str]:
		values = [file_format for file_format, enabled in format_vars.items() if enabled.get()]
		if not values:
			raise ValueError("Choose at least one format.")

		return sorted(values)

	def select_preset(name: str) -> None:
		values = set(presets[name])
		for size, enabled in size_vars.items():
			enabled.set(size in values)
		custom_sizes_var.set("")
		status_var.set(f"{name} preset selected.")
		update_summary()

	def update_summary(*_: object) -> None:
		try:
			sizes = selected_sizes()
			formats = selected_formats()
		except ValueError as error:
			summary_var.set(str(error))
			return

		source_name = Path(source_var.get()).name if source_var.get().strip() else "Not selected"
		output_text = relative_text(output_var.get().strip())
		names = [f"icon{size}.{file_format}" for size in sizes for file_format in formats]
		if copy_source_var.get() and source_var.get().strip():
			names.insert(0, source_name)

		visible_names = names[:10]
		extra = len(names) - len(visible_names)
		files_preview = "\n".join(f"  {name}" for name in visible_names)
		if extra > 0:
			files_preview += f"\n  ...and {extra} more"

		summary_var.set(
			f"Source: {source_name}\n"
			f"Output: {output_text}\n"
			f"Sizes: {', '.join(str(size) + 'px' for size in sizes)}\n"
			f"Formats: {', '.join(file_format.upper() for file_format in formats)}\n"
			f"Files: {len(names)}\n\n"
			f"{files_preview}"
		)

	def generate() -> None:
		try:
			source_text = source_var.get().strip()
			output_text = output_var.get().strip()
			if not source_text:
				raise ValueError("Choose a source image first.")
			if not output_text:
				raise ValueError("Choose an output folder.")

			source = validate_source(Path(source_text))
			output_dir = Path(output_text).expanduser()
			sizes = selected_sizes()
			formats = selected_formats()
			progress.start(10)
			generate_button.configure(state="disabled")
			status_var.set("Generating icons...")
			window.update_idletasks()
			created_files = create_icons(source, sizes, formats, output_dir, copy_source_var.get())
		except (RuntimeError, ValueError, FileExistsError) as error:
			messagebox.showerror("Could not generate icons", str(error))
			status_var.set(f"Error: {error}")
			return
		finally:
			progress.stop()
			generate_button.configure(state="normal")

		file_list = "\n".join(f"- {path.name}" for path in created_files[:12])
		if len(created_files) > 12:
			file_list += f"\n- ...and {len(created_files) - 12} more"

		messagebox.showinfo(
			"Icons generated",
			f"Created {len(created_files)} file(s) in:\n{output_dir}\n\n{file_list}",
		)
		status_var.set(f"Created {len(created_files)} file(s) in {output_dir}.")

	for variable in [source_var, output_var, custom_sizes_var, copy_source_var, *size_vars.values(), *format_vars.values()]:
		variable.trace_add("write", update_summary)

	container = ttk.Frame(window, padding=20, style="App.TFrame")
	container.pack(fill="both", expand=True)
	container.columnconfigure(0, weight=1)
	container.rowconfigure(1, weight=1)

	hero = ttk.Frame(container, padding=(24, 20), style="Hero.TFrame")
	hero.grid(row=0, column=0, sticky="ew", pady=(0, 18))
	hero.columnconfigure(0, weight=1)

	ttk.Label(hero, text="Icon Forge", style="HeroTitle.TLabel").grid(row=0, column=0, sticky="w")
	ttk.Label(
		hero,
		text="Turn one SVG or PNG into a clean icon pack for Chrome, PWA, favicon and custom exports.",
		style="HeroSub.TLabel",
	).grid(row=1, column=0, sticky="w", pady=(6, 0))

	content = ttk.Frame(container, style="App.TFrame")
	content.grid(row=1, column=0, sticky="nsew")
	content.columnconfigure(0, weight=3)
	content.columnconfigure(1, weight=2)
	content.rowconfigure(0, weight=1)

	left = ttk.Frame(content, style="App.TFrame")
	left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
	left.columnconfigure(0, weight=1)

	right = ttk.Frame(content, style="App.TFrame")
	right.grid(row=0, column=1, sticky="nsew")
	right.columnconfigure(0, weight=1)
	right.rowconfigure(0, weight=1)

	source_frame = ttk.LabelFrame(left, text="1. Pick the artwork", padding=16, style="Panel.TLabelframe")
	source_frame.grid(row=0, column=0, sticky="ew", pady=(0, 14))
	source_frame.columnconfigure(0, weight=1)
	ttk.Label(source_frame, text="Source image", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
	ttk.Label(source_frame, text="Use a square PNG for best results, or SVG if cairosvg is installed.", style="Muted.TLabel").grid(
		row=1,
		column=0,
		columnspan=2,
		sticky="w",
		pady=(2, 10),
	)
	ttk.Entry(source_frame, textvariable=source_var).grid(row=2, column=0, sticky="ew", padx=(0, 8))
	ttk.Button(source_frame, text="Browse", command=browse_source).grid(row=2, column=1)

	preset_frame = ttk.LabelFrame(left, text="2. Choose a preset", padding=16, style="Panel.TLabelframe")
	preset_frame.grid(row=1, column=0, sticky="ew", pady=(0, 14))
	for index, name in enumerate(presets):
		ttk.Button(
			preset_frame,
			text=name,
			style="Preset.TButton",
			command=lambda preset_name=name: select_preset(preset_name),
		).grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 8, 0))
		preset_frame.columnconfigure(index, weight=1)

	sizes_frame = ttk.LabelFrame(left, text="3. Fine tune sizes", padding=16, style="Panel.TLabelframe")
	sizes_frame.grid(row=2, column=0, sticky="ew", pady=(0, 14))
	for index, size in enumerate(DEFAULT_SIZES):
		ttk.Checkbutton(sizes_frame, text=f"{size}px", variable=size_vars[size]).grid(
			row=index // 3,
			column=index % 3,
			sticky="w",
			padx=(0, 24),
			pady=(0, 8),
		)
	ttk.Label(sizes_frame, text="Custom", style="Muted.TLabel").grid(row=2, column=0, sticky="w", pady=(8, 0))
	ttk.Entry(sizes_frame, textvariable=custom_sizes_var).grid(row=2, column=1, columnspan=2, sticky="ew", pady=(8, 0))
	ttk.Label(sizes_frame, text="Comma-separated, like 256,512", style="Muted.TLabel").grid(
		row=3,
		column=1,
		columnspan=2,
		sticky="w",
		pady=(4, 0),
	)
	sizes_frame.columnconfigure(2, weight=1)

	formats_frame = ttk.LabelFrame(left, text="4. Export options", padding=16, style="Panel.TLabelframe")
	formats_frame.grid(row=3, column=0, sticky="ew")
	for index, file_format in enumerate(sorted(SUPPORTED_FORMATS)):
		ttk.Checkbutton(formats_frame, text=file_format.upper(), variable=format_vars[file_format]).grid(
			row=0,
			column=index,
			sticky="w",
			padx=(0, 22),
		)
	ttk.Checkbutton(formats_frame, text="Copy original source", variable=copy_source_var).grid(
		row=1,
		column=0,
		columnspan=3,
		sticky="w",
		pady=(12, 0),
	)

	output_frame = ttk.LabelFrame(right, text="5. Destination", padding=16, style="Panel.TLabelframe")
	output_frame.grid(row=0, column=0, sticky="new", pady=(0, 14))
	output_frame.columnconfigure(0, weight=1)
	ttk.Label(output_frame, text="Output folder", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
	ttk.Label(output_frame, text="The app creates this folder. Existing folders are not overwritten.", style="Muted.TLabel").grid(
		row=1,
		column=0,
		columnspan=2,
		sticky="w",
		pady=(2, 10),
	)
	ttk.Entry(output_frame, textvariable=output_var).grid(row=2, column=0, sticky="ew", padx=(0, 8))
	ttk.Button(output_frame, text="Choose", command=browse_output).grid(row=2, column=1)

	summary_frame = ttk.LabelFrame(right, text="Preview", padding=16, style="Panel.TLabelframe")
	summary_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
	summary_frame.columnconfigure(0, weight=1)
	summary_frame.rowconfigure(1, weight=1)
	ttk.Label(summary_frame, text="Export summary", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
	ttk.Label(summary_frame, textvariable=summary_var, style="Summary.TLabel", justify="left").grid(
		row=1,
		column=0,
		sticky="nw",
		pady=(10, 0),
	)

	actions = ttk.Frame(container, style="App.TFrame")
	actions.grid(row=2, column=0, sticky="ew", pady=(18, 0))
	actions.columnconfigure(0, weight=1)
	ttk.Label(actions, textvariable=status_var, style="Status.TLabel").grid(row=0, column=0, sticky="w")
	progress = ttk.Progressbar(actions, mode="indeterminate", length=160)
	progress.grid(row=0, column=1, padx=(12, 12))
	generate_button = ttk.Button(actions, text="Generate Icons", style="Primary.TButton", command=generate)
	generate_button.grid(row=0, column=2, sticky="e")

	update_summary()

	window.mainloop()
	return 0


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Generate Chrome extension icon files from a PNG or SVG source.",
	)
	parser.add_argument("--source", help="Source .png or .svg file. If omitted, the script asks you to choose one.")
	parser.add_argument("--sizes", help="Comma-separated output sizes. Example: 16,48,96,128,192")
	parser.add_argument("--formats", help="Comma-separated output formats: png, webp, ico")
	parser.add_argument("--output", help="Output folder. If omitted, a timestamped folder is created.")
	parser.add_argument("--cli", action="store_true", help="Use the terminal wizard instead of the graphical interface.")
	parser.add_argument("--no-copy-source", action="store_true", help="Do not copy the original source image to the output folder.")
	return parser


def main() -> int:
	parser = build_parser()
	args = parser.parse_args()
	root = Path.cwd()
	uses_automation = any([args.source, args.sizes, args.formats, args.output])

	if not args.cli and not uses_automation:
		return run_gui(root)

	try:
		source = ask_source(root, args.source)
		sizes = ask_sizes(args.sizes)
		formats = ask_formats(args.formats)
		output_dir = ask_output_dir(root, args.output, source)
		created_files = create_icons(source, sizes, formats, output_dir, not args.no_copy_source)

	except (RuntimeError, ValueError, FileExistsError) as error:
		print(f"Error: {error}", file=sys.stderr)
		return 1

	print(f"\nCreated {len(created_files)} file(s) in {output_dir.relative_to(root) if output_dir.is_relative_to(root) else output_dir}:")
	for path in created_files:
		print(f"  - {path.name}")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())

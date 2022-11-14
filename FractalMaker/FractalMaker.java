import static java.lang.System.out;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.util.ArrayList;

import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JColorChooser;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JSlider;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;

import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class FractalMaker extends JPanel {
	
	private ArrayList<Line> lines;
	private JFrame frame;
	private JPanel sidePanel;
	private LeftPanel linesDrawnPanel;
	private LeftPanel totalLengthPanel;
	private JButton backgroundButton;
	private JButton treeButton;
	private Color backgroundColor;
	private Color treeColor;
	
	private JSlider xSlider;
	private JSlider ySlider;
	private JSlider lengthSlider;
	private JSlider lengthRatioSlider;
	private JSlider angleSlider;
	private JSlider branchesAngleSlider;
	private JSlider deltaAngleSlider;
	private JSlider branchesSlider;
	private JSlider branchesRatioSlider;
	private JSlider depthSlider;
	
	private JSpinner xSpinner;
	private JSpinner ySpinner;
	private JSpinner lengthSpinner;
	private JSpinner lengthRatioSpinner;
	private JSpinner angleSpinner;
	private JSpinner branchesAngleSpinner;
	private JSpinner deltaAngleSpinner;
	private JSpinner branchesSpinner;
	private JSpinner branchesRatioSpinner;
	private JSpinner depthSpinner;
	
	private int x1;
	private int y1;
	private double length;
	private double lengthRatio;
	private double angle;
	private double branchesAngle;
	private double deltaAngle;
	private int branches;
	private int branchesRatio;
	private int depth;
	
	static {
		out.println("Fractal Maker");
		out.println("Version 1.3");
		out.println("By Blake Herrera");
		out.println("");
		out.println("Feel free to leave feedback.");
		//Why use main
		//when you have
		//static initialization blocks?
	}
	
	{
		//TODO
		//Don't worry, this block will have a use later because
		//I plan on adding multiple fractal instances in the future
		//that way you can have overlapping fractals
		//and it'll be more awesome.
	}
	
	public FractalMaker() {
		frame = new JFrame("Fractal Maker v1.3");
		frame.setLayout(new BorderLayout());
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(2000, 1500);
		frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
		
		xSlider = new JSlider(-frame.getWidth(), frame.getWidth(), 400);
		xSlider.setMajorTickSpacing(100);
		xSlider.setPaintTicks(true);
		x1 = xSlider.getValue();
		xSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						x1 = xSlider.getValue();
						xSpinner.setValue(x1);
						redraw();
					}
				});
		xSpinner = new JSpinner(new SpinnerNumberModel(xSlider.getValue(), null, null, 1));
		xSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						x1 = (int)xSpinner.getValue();
						xSlider.setValue(x1);
						redraw();
					}
				});
		
		ySlider = new JSlider(-frame.getHeight(), frame.getHeight(), 300);
		ySlider.setMajorTickSpacing(100);
		ySlider.setPaintTicks(true);
		y1 = ySlider.getValue();
		ySlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						y1 = ySlider.getValue();
						ySpinner.setValue(y1);
						redraw();
					}
				});
		ySpinner = new JSpinner(new SpinnerNumberModel(ySlider.getValue(), null, null, 1));
		ySpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						y1 = (int)ySpinner.getValue();
						ySlider.setValue(y1);
						redraw();
					}
				});
		
		lengthSlider = new JSlider(0, 500, 100);
		lengthSlider.setMajorTickSpacing(50);
		lengthSlider.setPaintTicks(true);
		length = lengthSlider.getValue();
		lengthSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						length = lengthSlider.getValue();
						lengthSpinner.setValue(length);
						redraw();
					}
				});
		lengthSpinner = new JSpinner(new SpinnerNumberModel(100.0, 0.0, null, 1.0));
		lengthSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						length = (double)lengthSpinner.getValue();
						lengthSlider.setValue((int)length);
						redraw();
					}
				});
		
		lengthRatioSlider = new JSlider(0, 2000, 618);
		lengthRatioSlider.setMajorTickSpacing(100);
		lengthRatioSlider.setPaintTicks(true);
		lengthRatio = lengthRatioSlider.getValue() / 1000.0;
		lengthRatioSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						lengthRatio = lengthRatioSlider.getValue() / 1000.0;
						lengthRatioSpinner.setValue(lengthRatio);
						redraw();
					}
				});
		lengthRatioSpinner = new JSpinner(new SpinnerNumberModel(.618, 0.0, null, .01));
		lengthRatioSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						lengthRatio = (double)lengthRatioSpinner.getValue();
						lengthRatioSlider.setValue((int)(lengthRatio * 1000));
						redraw();
					}
				});
		
		angleSlider = new JSlider(0, 360, 90);
		angleSlider.setMajorTickSpacing(30);
		angleSlider.setPaintTicks(true);
		angle = angleSlider.getValue();
		angleSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						angle = angleSlider.getValue();
						angleSpinner.setValue(angle);
						redraw();
					}
				});
		angleSpinner = new JSpinner(new SpinnerNumberModel(90.0, 0.0, 360.0, 1.0));
		angleSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						angle = (double)angleSpinner.getValue();
						angleSlider.setValue((int)angle);
						redraw();
					}
				});
		
		branchesAngleSlider = new JSlider(0, 360, 60);
		branchesAngleSlider.setMajorTickSpacing(30);
		branchesAngleSlider.setPaintTicks(true);
		branchesAngle = branchesAngleSlider.getValue();
		branchesAngleSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						branchesAngle = branchesAngleSlider.getValue();
						branchesAngleSpinner.setValue(branchesAngle);
						redraw();
					}
				});
		branchesAngleSpinner = new JSpinner(new SpinnerNumberModel(60.0, 0.0, 360.0, 1.0));
		branchesAngleSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						branchesAngle = (double)branchesAngleSpinner.getValue();
						branchesAngleSlider.setValue((int)branchesAngle);
						redraw();
					}
				});
		
		deltaAngleSlider = new JSlider(0, 360, 0);
		deltaAngleSlider.setMajorTickSpacing(30);
		deltaAngleSlider.setPaintTicks(true);
		deltaAngle = deltaAngleSlider.getValue();
		deltaAngleSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						deltaAngle = deltaAngleSlider.getValue();
						deltaAngleSpinner.setValue(deltaAngle);
						redraw();
					}
				});
		deltaAngleSpinner = new JSpinner(new SpinnerNumberModel(0.0, 0.0, 360.0, 1.0));
		deltaAngleSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						deltaAngle = (double)deltaAngleSpinner.getValue();
						deltaAngleSlider.setValue((int)deltaAngle);
						redraw();
					}
				});
		
		branchesSlider = new JSlider(1, 10);
		branchesSlider.setMajorTickSpacing(1);
		branchesSlider.setPaintTicks(true);
		branches = branchesSlider.getValue();
		branchesSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						branches = branchesSlider.getValue();
						branchesSpinner.setValue(branches);
						redraw();
					}
				});
		branchesSpinner = new JSpinner(new SpinnerNumberModel(branchesSlider.getValue(), 1, null, 1));
		branchesSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						branches = (int)branchesSpinner.getValue();
						branchesSlider.setValue(branches);
						redraw();
					}
				});
		
		branchesRatioSlider = new JSlider(1, 10, 3);
		branchesRatioSlider.setMajorTickSpacing(1);
		branchesRatioSlider.setPaintTicks(true);
		branchesRatio = branchesRatioSlider.getValue();
		branchesRatioSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						branchesRatio = branchesRatioSlider.getValue();
						branchesRatioSpinner.setValue(branchesRatio);
						redraw();
					}
				});
		branchesRatioSpinner = new JSpinner(new SpinnerNumberModel(branchesRatioSlider.getValue(), 1, null, 1));
		branchesRatioSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						branchesRatio = (int)branchesRatioSpinner.getValue();
						branchesRatioSlider.setValue(branchesRatio);
						redraw();
					}
				});
		
		depthSlider = new JSlider(1, 10, 3);
		depthSlider.setMajorTickSpacing(1);
		depthSlider.setPaintTicks(true);
		depth = depthSlider.getValue();
		depthSlider.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						depth = depthSlider.getValue();
						depthSpinner.setValue(depth);
						redraw();
					}
				});
		depthSpinner = new JSpinner(new SpinnerNumberModel(depthSlider.getValue(), 1, null, 1));
		depthSpinner.addChangeListener(
				new ChangeListener() {
					public void stateChanged(ChangeEvent e) {
						depth = (int)depthSpinner.getValue();
						depthSlider.setValue(depth);
						redraw();
					}
				});
		
		backgroundColor = Color.WHITE;
		backgroundButton = new JButton("Choose background color");
		backgroundButton.addActionListener(
				new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						backgroundColor = JColorChooser.showDialog(null, "Choose background color", backgroundColor);
						setBackground(backgroundColor);
					}
				});
		
		treeColor = Color.BLACK;
		treeButton = new JButton("Choose tree color");
		treeButton.addActionListener(
				new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						treeColor = JColorChooser.showDialog(null, "Choose tree color", treeColor);
						redraw();
					}
				});
		
		lines = new ArrayList<>();
		sidePanel = new JPanel();
		sidePanel.setPreferredSize(new Dimension(300, 700));
		sidePanel.setLayout(new BoxLayout(sidePanel, BoxLayout.PAGE_AXIS));
		sidePanel.add(new LeftPanel("Version 1.3 - by Blake Herrera"));
		sidePanel.add(new TextSpinnerPanel(new JLabel("x position"), xSpinner));
		sidePanel.add(xSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("y position"), ySpinner));
		sidePanel.add(ySlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("zoom"), lengthSpinner));
		sidePanel.add(lengthSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("length ratio"), lengthRatioSpinner));
		sidePanel.add(lengthRatioSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("rotation"), angleSpinner));
		sidePanel.add(angleSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("angle between branches"), branchesAngleSpinner));
		sidePanel.add(branchesAngleSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("change in angle"), deltaAngleSpinner));
		sidePanel.add(deltaAngleSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("initial branches"), branchesSpinner));
		sidePanel.add(branchesSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("branches ratio"), branchesRatioSpinner));
		sidePanel.add(branchesRatioSlider);
		sidePanel.add(new TextSpinnerPanel(new JLabel("depth"), depthSpinner));
		sidePanel.add(depthSlider);
		
		sidePanel.add(new LeftPanel(backgroundButton));
		sidePanel.add(new LeftPanel(treeButton));
		linesDrawnPanel = new LeftPanel("Lines drawn: 0");
		sidePanel.add(linesDrawnPanel);
		totalLengthPanel = new LeftPanel("Total length: 0.0");
		sidePanel.add(totalLengthPanel);
		
		frame.add(this, BorderLayout.CENTER);
		frame.add(new JScrollPane(sidePanel), BorderLayout.WEST);
		//frame.add(sidePanel, BorderLayout.WEST);
		frame.setVisible(true);
		setBackground(Color.WHITE);
		
		redraw();
	}
	
	public static void main(String[] args) {
		new FractalMaker();
	}
	
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		g.setColor(treeColor);
		
		for(Line l:lines){
			g.drawLine(
				(int)Math.round(l.x1), 
				(int)Math.round(this.getHeight() - l.y1), 
				(int)Math.round(l.x2), 
				(int)Math.round(this.getHeight() - l.y2)
			);
		}
	}
	
	public void redraw() {
		try{
			lines = new ArrayList<>();
			setLines(
				x1,
				y1,
				length,
				lengthRatio,
				angle,
				branchesAngle,
				deltaAngle,
				branches,
				branchesRatio,
				depth
			);
			validate();
			repaint();
			sidePanel.remove(linesDrawnPanel);
			linesDrawnPanel = new LeftPanel("Lines drawn: " + lines.size());
			sidePanel.add(linesDrawnPanel);
			sidePanel.remove(totalLengthPanel);
			totalLengthPanel = new LeftPanel("Total length: Calculating...");
			sidePanel.add(totalLengthPanel);
			sidePanel.validate();
			sidePanel.repaint();
			double len = 0;
			for(Line c : lines) {
				len += c.len;
			}
			len /= lines.get(0).len;
			sidePanel.remove(totalLengthPanel);
			totalLengthPanel = new LeftPanel("Total length: " + (long)len + new Double(len % 1).toString().substring(1));
			sidePanel.add(totalLengthPanel);
			sidePanel.validate();
			sidePanel.repaint();
		} catch(Exception e) {
			e.printStackTrace();
			JOptionPane.showMessageDialog(null, "A fatal error has occurred when redrawing lines.\nSystem will now exit.", "Error", JOptionPane.ERROR_MESSAGE);
			System.exit(0);
		}
	}
	
	public void setLines(
			double x1,
			double y1,
			double length, 
			double lengthRatio,
			double angle, 
			double branchesAngle,
			double deltaAngle,
			int branches, 
			int branchesRatio,
			int depth
			) {
		for(int c=0;c<branches;c++) {
			if(depth > 0) {
				Line l = new Line(x1, y1, length, angle + branchesAngle * c);
				lines.add(l);
				//dat recursion
				setLines(
						l.x2,
						l.y2,
						length * lengthRatio,
						lengthRatio,
						angle + deltaAngle + branchesAngle * c - (branches * branchesRatio - 1) * branchesAngle / 2,
						branchesAngle,
						deltaAngle,
						branches * branchesRatio,
						branchesRatio,
						depth - 1
				);
			}
		}
	}
	
	private class Line {
		
		private double x1;
		private double y1;
		private double x2;
		private double y2;
		private double len;
		
		
		public Line(double x, double y, double len, double angle) {
			x1 = x;
			y1 = y;
			x2 = x + len * Math.cos(Math.toRadians(angle));
			y2 = y + len * Math.sin(Math.toRadians(angle));
			this.len = len;
		}
		
		public String toString() {
			return "(" + x1 + ", " + y1 + ") (" + x2 + ", " + y2 + ")";
		}
	}
	
	//The result of my frustration with JSpinner
	private class TextSpinnerPanel extends JPanel {
		
		public TextSpinnerPanel(JComponent first, JComponent second) {
			setLayout(new BorderLayout());
			add(first, BorderLayout.LINE_START);
			second.setPreferredSize(new Dimension(80, second.getHeight()));
			add(second, BorderLayout.LINE_END);
		}
	}
	
	//I got lazy with the layouts so I did this
	private class LeftPanel extends JPanel {
		
		public LeftPanel(JComponent component) {
			setLayout(new BorderLayout());
			add(component, BorderLayout.LINE_START);
			add(new JLabel(""), BorderLayout.LINE_END);
		}
		
		public LeftPanel(String s) {
			this(new JLabel(s));
		}
	}
}	
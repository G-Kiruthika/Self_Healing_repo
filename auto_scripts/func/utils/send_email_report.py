"""Utility module for sending email reports."""

import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


def load_email_config():
    """Load email configuration from config.yaml.
    
    Returns:
        dict: Email configuration
    """
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        return config.get('email', {})


def send_report(message, subject=None, attachment_path=None):
    """Send email report.
    
    Args:
        message: Email message body
        subject: Email subject (optional, uses config default)
        attachment_path: Path to attachment file (optional)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        config = load_email_config()
        
        if not config.get('enabled', False):
            print("Email reporting is disabled in configuration.")
            return False
        
        # Email configuration
        smtp_server = config.get('smtp_server')
        smtp_port = config.get('smtp_port')
        sender = config.get('sender')
        recipients = config.get('recipients', [])
        email_subject = subject or config.get('subject', 'Test Automation Report')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = email_subject
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            # Note: Add authentication if required
            # server.login(username, password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {recipients}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_test_report(test_results, report_path=None):
    """Send test execution report.
    
    Args:
        test_results: Dictionary containing test results
        report_path: Path to HTML report file (optional)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Format test results message
    total = test_results.get('total', 0)
    passed = test_results.get('passed', 0)
    failed = test_results.get('failed', 0)
    skipped = test_results.get('skipped', 0)
    
    message = f"""
    Test Automation Report
    =====================
    
    Total Tests: {total}
    Passed: {passed}
    Failed: {failed}
    Skipped: {skipped}
    
    Success Rate: {(passed/total*100):.2f}%
    
    Please find the detailed report attached.
    """
    
    return send_report(message, attachment_path=report_path)

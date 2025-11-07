"""
Inversión de Dependencias para Procesadores de Pago
====================================================

Este módulo implementa el principio de Inversión de Dependencias (Dependency Inversion Principle)
mediante una interfaz abstracta y múltiples implementaciones concretas.

Componentes:
- PaymentProcessor: Interfaz abstracta (clase base abstracta)
- CardPaymentProcessor: Implementación para pagos con tarjeta
- CheckPaymentProcessor: Implementación para pagos con cheque (genera PDF)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from decimal import Decimal
from django.conf import settings
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime


class PaymentResult:
    """Clase para encapsular el resultado de un procesamiento de pago"""
    
    def __init__(self, success: bool, message: str, transaction_id: str = None, pdf_data: bytes = None):
        self.success = success
        self.message = message
        self.transaction_id = transaction_id
        self.pdf_data = pdf_data
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'message': self.message,
            'transaction_id': self.transaction_id,
            'has_pdf': self.pdf_data is not None
        }


class PaymentProcessor(ABC):
    """
    Interfaz abstracta para procesadores de pago.
    
    Esta clase define el contrato que todas las implementaciones concretas
    deben cumplir, siguiendo el principio de Inversión de Dependencias.
    """
    
    @abstractmethod
    def process_payment(self, user, order, amount: Decimal) -> PaymentResult:
        """
        Procesa un pago para una orden específica.
        
        Args:
            user: Usuario que realiza el pago
            order: Orden a pagar
            amount: Monto a pagar
            
        Returns:
            PaymentResult: Resultado del procesamiento del pago
        """
        pass
    
    @abstractmethod
    def validate_payment(self, user, amount: Decimal) -> tuple[bool, str]:
        """
        Valida si el pago puede ser procesado.
        
        Args:
            user: Usuario que realiza el pago
            amount: Monto a pagar
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        pass
    
    @abstractmethod
    def get_payment_method_name(self) -> str:
        """Retorna el nombre del método de pago"""
        pass


class CardPaymentProcessor(PaymentProcessor):
    """
    Implementación concreta para pagos con tarjeta.
    
    Esta implementación simula un pago con tarjeta descontando el monto
    del balance disponible del usuario.
    """
    
    def get_payment_method_name(self) -> str:
        return "Tarjeta de Crédito/Débito"
    
    def validate_payment(self, user, amount: Decimal) -> tuple[bool, str]:
        """Valida que el usuario tenga saldo suficiente"""
        if not hasattr(user, 'balance'):
            return False, "El usuario no tiene un balance configurado"
        
        if user.balance < amount:
            return False, f"Saldo insuficiente. Saldo disponible: ${user.balance:.2f}, Monto requerido: ${amount:.2f}"
        
        return True, ""
    
    def process_payment(self, user, order, amount: Decimal) -> PaymentResult:
        """
        Procesa el pago descontando del balance del usuario.
        
        Simula una transacción real con tarjeta:
        1. Valida el saldo disponible
        2. Descuenta el monto del balance
        3. Genera un ID de transacción
        4. Actualiza el estado de la orden
        """
        # Validar el pago
        is_valid, error_message = self.validate_payment(user, amount)
        if not is_valid:
            return PaymentResult(
                success=False,
                message=error_message
            )
        
        try:
            # Descontar del balance del usuario
            user.balance -= amount
            user.save()
            
            # Generar ID de transacción
            transaction_id = f"CARD-{order.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Actualizar estado de la orden
            order.status = 'paid'
            order.save()
            
            return PaymentResult(
                success=True,
                message=f"Pago procesado exitosamente. Nuevo saldo: ${user.balance:.2f}",
                transaction_id=transaction_id
            )
            
        except Exception as e:
            return PaymentResult(
                success=False,
                message=f"Error al procesar el pago: {str(e)}"
            )


class CheckPaymentProcessor(PaymentProcessor):
    """
    Implementación concreta para pagos con cheque.
    
    Esta implementación genera un PDF con la información del cheque
    que el usuario debe utilizar para realizar el pago.
    """
    
    def get_payment_method_name(self) -> str:
        return "Cheque Bancario"
    
    def validate_payment(self, user, amount: Decimal) -> tuple[bool, str]:
        """
        Valida información básica del usuario.
        El cheque no requiere validación de fondos inmediatos.
        """
        if not user.first_name or not user.last_name:
            return False, "El usuario debe tener nombre y apellido configurados"
        
        if amount <= 0:
            return False, "El monto debe ser mayor a cero"
        
        return True, ""
    
    def _generate_check_pdf(self, user, order, amount: Decimal, check_number: str) -> bytes:
        """
        Genera un PDF con el formato de un cheque bancario.
        
        Returns:
            bytes: Contenido del PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        # Título
        elements.append(Paragraph("CHEQUE BANCARIO", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Información del banco (simulado)
        bank_info = [
            ["BANCO ALTA RAZA", ""],
            ["Sucursal: Principal", f"Fecha: {datetime.now().strftime('%d/%m/%Y')}"],
            ["", f"Cheque No: {check_number}"]
        ]
        
        bank_table = Table(bank_info, colWidths=[4*inch, 2.5*inch])
        bank_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        elements.append(bank_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Línea separadora
        elements.append(Paragraph("_" * 80, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Monto
        elements.append(Paragraph(f"<b>PÁGUESE A LA ORDEN DE:</b> Urban Loom S.A.", header_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Formatear monto en pesos colombianos
        formatted_amount = f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        amount_text = f"<b>MONTO:</b> ${formatted_amount} COP"
        elements.append(Paragraph(amount_text, ParagraphStyle(
            'Amount',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#27ae60')
        )))
        elements.append(Spacer(1, 0.3*inch))
        
        # Convertir monto a texto (simplificado)
        amount_words = self._amount_to_words(float(amount))
        elements.append(Paragraph(f"<i>({amount_words} pesos colombianos)</i>", styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Información del pagador
        elements.append(Paragraph("<b>INFORMACIÓN DEL PAGADOR:</b>", header_style))
        payer_data = [
            ["Nombre:", f"{user.first_name} {user.last_name}"],
            ["Email:", user.email],
            ["Teléfono:", user.phone_number or "N/A"],
            ["Orden:", f"#{order.id}"],
        ]
        
        payer_table = Table(payer_data, colWidths=[1.5*inch, 5*inch])
        payer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ]))
        elements.append(payer_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Firma
        elements.append(Spacer(1, 0.8*inch))
        elements.append(Paragraph("_" * 50, ParagraphStyle(
            'SignatureLine',
            parent=styles['Normal'],
            alignment=1  # Center
        )))
        elements.append(Paragraph("<b>Firma del Titular</b>", ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            alignment=1  # Center
        )))
        elements.append(Spacer(1, 0.3*inch))
        
        # Salto de página antes de las instrucciones
        elements.append(PageBreak())
        
        # Instrucciones
        elements.append(Paragraph("<b>INSTRUCCIONES:</b>", header_style))
        instructions = """
        1. Imprima este cheque en papel tamaño carta.<br/>
        2. Firme en el espacio indicado.<br/>
        3. Presente el cheque en cualquier sucursal de Urban Loom.<br/>
        4. Su orden será procesada una vez validado el cheque.<br/>
        5. Conserve una copia para sus registros.
        """
        elements.append(Paragraph(instructions, styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def _amount_to_words(self, amount: float) -> str:
        """Convierte un monto numérico a palabras (versión simplificada)"""
        # Esta es una versión simplificada. En producción usarías una librería como num2words
        integer_part = int(amount)
        decimal_part = int((amount - integer_part) * 100)
        
        if integer_part == 0:
            return f"Cero con {decimal_part:02d}/100"
        
        # Simplificación: solo maneja números hasta 9999
        units = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
        tens = ["", "diez", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
        
        if integer_part < 10:
            words = units[integer_part]
        elif integer_part < 100:
            ten = integer_part // 10
            unit = integer_part % 10
            words = f"{tens[ten]}" + (f" y {units[unit]}" if unit > 0 else "")
        else:
            words = str(integer_part)
        
        return f"{words.capitalize()}"
    
    def process_payment(self, user, order, amount: Decimal) -> PaymentResult:
        """
        Procesa el pago generando un PDF con el cheque.
        
        NO descuenta fondos inmediatamente, pero genera el documento
        necesario para que el usuario complete el pago.
        """
        # Validar el pago
        is_valid, error_message = self.validate_payment(user, amount)
        if not is_valid:
            return PaymentResult(
                success=False,
                message=error_message
            )
        
        try:
            # Generar número de cheque
            check_number = f"CHK-{order.id:06d}-{datetime.now().strftime('%Y%m%d')}"
            
            # Generar PDF del cheque
            pdf_data = self._generate_check_pdf(user, order, amount, check_number)
            
            # La orden queda en estado "pending" hasta que se valide el cheque
            order.status = 'pending'
            order.save()
            
            return PaymentResult(
                success=True,
                message=f"Cheque generado exitosamente. Número de cheque: {check_number}. Por favor, descargue e imprima el cheque.",
                transaction_id=check_number,
                pdf_data=pdf_data
            )
            
        except Exception as e:
            return PaymentResult(
                success=False,
                message=f"Error al generar el cheque: {str(e)}"
            )


# Factory para crear procesadores de pago
class PaymentProcessorFactory:
    """
    Factory para crear instancias de procesadores de pago.
    
    Esto permite desacoplar la lógica de negocio de las implementaciones
    concretas de los procesadores.
    """
    
    _processors = {
        'card': CardPaymentProcessor,
        'check': CheckPaymentProcessor,
    }
    
    @classmethod
    def create(cls, payment_method: str) -> PaymentProcessor:
        """
        Crea una instancia del procesador de pago solicitado.
        
        Args:
            payment_method: Tipo de método de pago ('card' o 'check')
            
        Returns:
            PaymentProcessor: Instancia del procesador correspondiente
            
        Raises:
            ValueError: Si el método de pago no es válido
        """
        processor_class = cls._processors.get(payment_method)
        if not processor_class:
            raise ValueError(f"Método de pago no válido: {payment_method}. Opciones: {list(cls._processors.keys())}")
        
        return processor_class()
    
    @classmethod
    def get_available_methods(cls) -> Dict[str, str]:
        """Retorna los métodos de pago disponibles y sus nombres"""
        return {
            key: processor_class().get_payment_method_name()
            for key, processor_class in cls._processors.items()
        }
